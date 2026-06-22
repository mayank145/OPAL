"""
Summit Logging business logic — legacy MariaDB `sumlogs` (days, items, progs).
"""
from __future__ import annotations

import asyncio
import re
import smtplib
from datetime import date, datetime, timezone
from email.mime.text import MIMEText
from typing import Any, Dict, List, Optional, Tuple

from fastapi import HTTPException
from sqlalchemy import delete, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.summit_legacy import Day, Item, ItemReq, Prog
from app.services import summit_legacy_mapper as mapper
from app.services.summit_legacy_mapper import _parse_int


def _strip_nul(v: Optional[str]) -> Optional[str]:
    if v is None:
        return None
    return v.replace("\x00", "") if "\x00" in v else v


def _parse_float(s: Any) -> Optional[float]:
    if s is None or s == "":
        return None
    try:
        return float(str(s).strip())
    except (ValueError, TypeError):
        return None


class SummitService:

    async def _get_day_row(self, db: AsyncSession, log_date: date) -> Day:
        row = (await db.execute(select(Day).where(Day.date == log_date))).scalar_one_or_none()
        if not row:
            raise HTTPException(status_code=404, detail=f"Summit day not found for {log_date}")
        return row

    async def _get_day_by_idno(self, db: AsyncSession, dayidno: int) -> Day:
        row = (await db.execute(select(Day).where(Day.idno == dayidno))).scalar_one_or_none()
        if not row:
            raise HTTPException(status_code=404, detail="Summit day not found")
        return row

    async def _req_codes_for_wp(self, db: AsyncSession, plan_idno: int) -> List[str]:
        rows = (await db.execute(select(ItemReq.code).where(ItemReq.planidno == plan_idno))).all()
        return [r[0] for r in rows if r[0]]

    async def _req_codes_batch(self, db: AsyncSession, plan_idnos: List[int]) -> Dict[int, List[str]]:
        """Fetch itemreqs for multiple WPs in a single query (avoids N+1)."""
        if not plan_idnos:
            return {}
        rows = (await db.execute(
            select(ItemReq.planidno, ItemReq.code).where(ItemReq.planidno.in_(plan_idnos))
        )).all()
        result: Dict[int, List[str]] = {pid: [] for pid in plan_idnos}
        for pid, code in rows:
            if code:
                result[pid].append(code)
        return result

    async def _set_req_codes(self, db: AsyncSession, plan_idno: int, req_flags: Optional[str], lockout_flags: Optional[str]) -> None:
        await db.execute(delete(ItemReq).where(ItemReq.planidno == plan_idno))
        codes: List[str] = []
        for blob, is_lock in ((req_flags, False), (lockout_flags, True)):
            if not blob:
                continue
            for part in str(blob).split(","):
                code = part.strip()
                if code:
                    codes.append(code)
        for code in codes:
            db.add(ItemReq(planidno=plan_idno, code=code))

    # ── Days ────────────────────────────────────────────────────────────────────

    async def get_monthly_days(self, db: AsyncSession, year: int, month: int) -> List[dict]:
        start = date(year, month, 1)
        end = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
        days = list(
            (await db.execute(select(Day).where(Day.date >= start, Day.date < end).order_by(Day.date))).scalars().all()
        )
        if not days:
            return []

        day_ids = [d.idno for d in days]
        counts = (
            await db.execute(
                select(Item.dayidno, func.count(Item.idno), func.coalesce(func.sum(Item.downtime), 0))
                .where(Item.dayidno.in_(day_ids), Item.logcrew != "WP")
                .group_by(Item.dayidno)
            )
        ).all()
        counts_map = {r[0]: (r[1], r[2]) for r in counts}

        out = []
        for d in days:
            ec, dt = counts_map.get(d.idno, (0, 0))
            out.append({"day": mapper.day_to_api(d), "entry_count": ec, "total_downtime": int(dt or 0)})
        return out

    async def get_yearly_days(self, db: AsyncSession, year: int) -> List[dict]:
        start = date(year, 1, 1)
        end = date(year + 1, 1, 1)
        days = list(
            (await db.execute(select(Day).where(Day.date >= start, Day.date < end).order_by(Day.date))).scalars().all()
        )
        if not days:
            return []

        day_ids = [d.idno for d in days]
        counts = (
            await db.execute(
                select(Item.dayidno, func.count(Item.idno), func.coalesce(func.sum(Item.downtime), 0))
                .where(Item.dayidno.in_(day_ids), Item.logcrew != "WP")
                .group_by(Item.dayidno)
            )
        ).all()
        counts_map = {r[0]: (r[1], r[2]) for r in counts}

        first_instr: Dict[int, str] = {}
        for row in (
            await db.execute(
                select(Prog.dayidno, Prog.instr, Prog.seq)
                .where(Prog.dayidno.in_(day_ids))
                .order_by(Prog.dayidno, Prog.seq)
            )
        ).all():
            if row.dayidno not in first_instr and row.instr:
                first_instr[row.dayidno] = row.instr.strip()

        out = []
        for d in days:
            ec, dt = counts_map.get(d.idno, (0, 0))
            out.append({
                "day": mapper.day_to_api(d),
                "entry_count": ec,
                "total_downtime": int(dt or 0),
                "first_instr": first_instr.get(d.idno),
            })
        return out

    async def create_summit_day(self, db: AsyncSession, log_date: date, day_label: Optional[str], history_text: Optional[str]) -> dict:
        if (await db.execute(select(Day).where(Day.date == log_date))).scalar_one_or_none():
            raise HTTPException(status_code=409, detail=f"Summit day already exists for {log_date}")
        day = Day(date=log_date, day=_strip_nul(day_label), history=_strip_nul(history_text))
        db.add(day)
        await db.commit()
        await db.refresh(day)
        return mapper.day_to_api(day)

    async def get_daily_view(self, db: AsyncSession, log_date: date) -> dict:
        day = await self._get_day_row(db, log_date)
        items = list(
            (await db.execute(select(Item).where(Item.dayidno == day.idno).order_by(Item.itemtime, Item.idno))).scalars().all()
        )
        progs = list(
            (await db.execute(select(Prog).where(Prog.dayidno == day.idno).order_by(Prog.seq, Prog.idno))).scalars().all()
        )

        log_items = [mapper.log_item_to_api(i) for i in items if mapper.is_log_item(i)]
        wp_items = [i for i in items if mapper.is_work_plan(i)]
        codes_map = await self._req_codes_batch(db, [i.idno for i in wp_items])
        work_plans = [mapper.work_plan_to_api(i, codes_map.get(i.idno, [])) for i in wp_items]

        entry_count = len(log_items)
        total_downtime = sum(_parse_int(li.get("downtime_minutes")) for li in log_items)

        return {
            "day": mapper.day_to_api(day),
            "crew": mapper.crew_from_day(day),
            "weather": mapper.weather_from_day(day),
            "programs": [mapper.prog_to_api(p) for p in progs],
            "work_plans": work_plans,
            "log_items": log_items,
            "email_delivery": mapper.email_from_day(day),
            "entry_count": entry_count,
            "total_downtime": total_downtime,
        }

    async def update_summit_day(self, db: AsyncSession, log_date: date, data: dict[str, Any]) -> dict:
        day = await self._get_day_row(db, log_date)
        if "day_label" in data:
            day.day = _strip_nul(data["day_label"])
        if "history_text" in data:
            day.history = _strip_nul(data["history_text"])
        # Zoom fields are API-only; legacy `days` table has no zoom columns on this server.
        await db.commit()
        await db.refresh(day)
        return mapper.day_to_api(day)

    async def get_summit_day_by_date(self, db: AsyncSession, log_date: date) -> dict:
        return mapper.day_to_api(await self._get_day_row(db, log_date))

    # ── Crew (stored on `days` row) ─────────────────────────────────────────────

    async def get_crew(self, db: AsyncSession, crew_id: str) -> dict:
        slot = mapper.CREW_SLOT_BY_ID.get(crew_id)
        if not slot:
            raise HTTPException(status_code=404, detail="Crew assignment not found")
        raise HTTPException(status_code=400, detail="Use day view to resolve crew by slot id")

    async def create_crew(self, db: AsyncSession, log_date: date, data: dict[str, Any]) -> dict:
        day = await self._get_day_row(db, log_date)
        role = data["role"].strip().upper()
        slots = [s for s in mapper.CREW_SLOTS if s["role"] == role]
        target = None
        for slot in slots:
            if not getattr(day, slot["name"], None):
                target = slot
                break
        if not target:
            raise HTTPException(status_code=409, detail=f"No empty {role} crew slot on this day")
        setattr(day, target["name"], _strip_nul(data.get("member_name")))
        if target["loc"] and "location" in data:
            setattr(day, target["loc"], _strip_nul(data.get("location")))
        if target["tin"] and "time_in" in data:
            setattr(day, target["tin"], data.get("time_in"))
        if target["tout"] and "time_out" in data:
            setattr(day, target["tout"], data.get("time_out"))
        await db.commit()
        await db.refresh(day)
        for c in mapper.crew_from_day(day):
            if c["id"] == target["id"]:
                return c
        raise HTTPException(status_code=500, detail="Crew slot update failed")

    async def update_crew(self, db: AsyncSession, crew_id: str, data: dict[str, Any]) -> dict:
        slot = mapper.CREW_SLOT_BY_ID.get(crew_id)
        if not slot:
            raise HTTPException(status_code=404, detail="Crew assignment not found")
        dayidno = data.pop("_dayidno", None)
        if dayidno is None:
            raise HTTPException(status_code=400, detail="Internal: day id required")
        day = await self._get_day_by_idno(db, dayidno)
        if "member_name" in data:
            setattr(day, slot["name"], _strip_nul(data["member_name"]))
        if slot["loc"] and "location" in data:
            setattr(day, slot["loc"], _strip_nul(data.get("location")))
        if slot["tin"] and "time_in" in data:
            setattr(day, slot["tin"], data.get("time_in"))
        if slot["tout"] and "time_out" in data:
            setattr(day, slot["tout"], data.get("time_out"))
        await db.commit()
        await db.refresh(day)
        for c in mapper.crew_from_day(day):
            if c["id"] == crew_id:
                return c
        return {"id": crew_id, "summit_day_id": day.idno, "role": slot["role"], "sort_order": slot["sort"]}

    async def update_crew_by_id(self, db: AsyncSession, log_date: date, crew_id: str, data: dict[str, Any]) -> dict:
        data = {**data, "_dayidno": (await self._get_day_row(db, log_date)).idno}
        return await self.update_crew(db, crew_id, data)

    async def delete_crew(self, db: AsyncSession, log_date: date, crew_id: str) -> None:
        slot = mapper.CREW_SLOT_BY_ID.get(crew_id)
        if not slot:
            raise HTTPException(status_code=404, detail="Crew assignment not found")
        day = await self._get_day_row(db, log_date)
        setattr(day, slot["name"], None)
        if slot["loc"]:
            setattr(day, slot["loc"], None)
        if slot["tin"]:
            setattr(day, slot["tin"], None)
        if slot["tout"]:
            setattr(day, slot["tout"], None)
        await db.commit()

    # ── Weather (on `days` row) ─────────────────────────────────────────────────

    async def upsert_weather(self, db: AsyncSession, log_date: date, data: dict[str, Any]) -> dict:
        day = await self._get_day_row(db, log_date)
        for api_field, col in (
            ("sky", "sky"), ("seeing", "seeing"), ("wind", "wind"),
            ("comment_text", "comment"),
        ):
            if api_field in data:
                setattr(day, col, _strip_nul(data[api_field]))
        if "temp_raw" in data:
            day.temp = _strip_nul(data["temp_raw"])
        if "humidity_raw" in data:
            day.humid = _strip_nul(data["humidity_raw"])
        await db.commit()
        await db.refresh(day)
        return mapper.weather_from_day(day) or {"id": day.idno}

    # ── Programs (`progs`) ──────────────────────────────────────────────────────

    async def get_program(self, db: AsyncSession, program_id: int) -> dict:
        row = (await db.execute(select(Prog).where(Prog.idno == program_id))).scalar_one_or_none()
        if not row:
            raise HTTPException(status_code=404, detail="Program not found")
        return mapper.prog_to_api(row)

    def _apply_program(self, prog: Prog, data: dict[str, Any]) -> None:
        mapping = {
            "instr": "instr", "alloc": "alloc", "pi": "pi", "ao1": "ao1", "ao2": "ao2",
            "gid": "gid", "propid": "propid",
            "obs1": "obs1", "obs1loc": "obs1loc", "obs2": "obs2", "obs2loc": "obs2loc",
            "obs3": "obs3", "obs3loc": "obs3loc", "obs4": "obs4", "obs4loc": "obs4loc",
            "ss": "ss", "ssloc": "ssloc", "ss2": "ss2", "ss2loc": "ss2loc",
            "others1": "others1", "others1loc": "others1loc", "others2": "others2", "others2loc": "others2loc",
            "comment_text": "comment",
        }
        for api_f, col in mapping.items():
            if api_f in data:
                setattr(prog, col, _strip_nul(data[api_f]))
        if "slot_start" in data:
            prog.intime = data["slot_start"]
        if "slot_end" in data:
            prog.outtime = data["slot_end"]
        if "sort_order" in data and data["sort_order"] is not None:
            n = int(data["sort_order"])
            prog.seq = chr(ord("A") + n) if 0 <= n < 26 else str(n)

    async def create_program(self, db: AsyncSession, log_date: date, data: dict[str, Any]) -> dict:
        day = await self._get_day_row(db, log_date)
        prog = Prog(dayidno=day.idno, date=log_date, seq="A")
        self._apply_program(prog, data)
        db.add(prog)
        await db.commit()
        await db.refresh(prog)
        return mapper.prog_to_api(prog)

    async def update_program(self, db: AsyncSession, program_id: int, data: dict[str, Any]) -> dict:
        prog = (await db.execute(select(Prog).where(Prog.idno == program_id))).scalar_one_or_none()
        if not prog:
            raise HTTPException(status_code=404, detail="Program not found")
        self._apply_program(prog, data)
        await db.commit()
        await db.refresh(prog)
        return mapper.prog_to_api(prog)

    async def delete_program(self, db: AsyncSession, program_id: int) -> None:
        await self.get_program(db, program_id)
        await db.execute(delete(Prog).where(Prog.idno == program_id))
        await db.commit()

    # ── Work plans (items where logcrew='WP') ───────────────────────────────────

    async def get_work_plan(self, db: AsyncSession, plan_id: int) -> dict:
        row = (await db.execute(select(Item).where(Item.idno == plan_id, Item.logcrew == "WP"))).scalar_one_or_none()
        if not row:
            raise HTTPException(status_code=404, detail="Work plan not found")
        codes = await self._req_codes_for_wp(db, plan_id)
        return mapper.work_plan_to_api(row, codes)

    def _apply_wp(self, item: Item, data: dict[str, Any]) -> None:
        field_map = {
            "requestor": "contact1", "wp_status": "status", "wp_type": "type", "wp_subsystem": "subsystem",
            "plan_text": "itemtext", "day_warning": "comment", "teampass": "pass_",
            "window_start": "itemtime", "window_end": "endtime",
            "realstart": "realstart", "realend": "realend",
            "nite_effect": "niteeffect", "day_effect": "dayeffect",
            "location": "location", "location2": "location2", "location3": "location3",
            "assigned1": "assigned1", "assigned2": "assigned2", "dcassist": "dcassist",
            "notify": "notify", "contact1": "contact1", "contact2": "contact2",
            "others": "others", "otherreq": "otherreq", "comptitle": "comptitle",
            "intervene": "intervene", "melco": "melco", "fai": "fai",
            "pass_text": "pass_", "rpass_text": "rpass", "requirements": "otherreq",
        }
        for api_f, col in field_map.items():
            if api_f in data:
                val = _strip_nul(data[api_f]) if isinstance(data[api_f], str) else data[api_f]
                setattr(item, col, val)
        for f in ("master", "seats", "seats2", "pseats"):
            if f in data:
                setattr(item, f, data[f])
        if "req_flags" in data or "lockout_flags" in data:
            item._pending_req = (data.get("req_flags"), data.get("lockout_flags"))  # type: ignore[attr-defined]

    async def create_work_plan(self, db: AsyncSession, log_date: date, data: dict[str, Any]) -> dict:
        day = await self._get_day_row(db, log_date)
        item = Item(dayidno=day.idno, date=log_date, day=day.day, logcrew="WP", status="Planned", timestamp=datetime.now())
        self._apply_wp(item, data)
        pending = getattr(item, "_pending_req", (None, None))
        db.add(item)
        await db.flush()
        await self._set_req_codes(db, item.idno, pending[0], pending[1])
        await db.commit()
        await db.refresh(item)
        codes = await self._req_codes_for_wp(db, item.idno)
        return mapper.work_plan_to_api(item, codes)

    async def update_work_plan(self, db: AsyncSession, plan_id: int, data: dict[str, Any]) -> dict:
        item = (await db.execute(select(Item).where(Item.idno == plan_id, Item.logcrew == "WP"))).scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Work plan not found")
        self._apply_wp(item, data)
        pending = getattr(item, "_pending_req", None)
        if pending is not None:
            await self._set_req_codes(db, plan_id, pending[0], pending[1])
        await db.commit()
        await db.refresh(item)
        return mapper.work_plan_to_api(item, await self._req_codes_for_wp(db, plan_id))

    async def delete_work_plan(self, db: AsyncSession, plan_id: int) -> None:
        await self.get_work_plan(db, plan_id)
        await db.execute(delete(ItemReq).where(ItemReq.planidno == plan_id))
        await db.execute(delete(Item).where(Item.idno == plan_id))
        await db.commit()

    async def get_recent_work_plans(self, db: AsyncSession, username: str, limit: int = 20) -> List[dict]:
        stmt = (
            select(Item, Day.date)
            .join(Day, Item.dayidno == Day.idno)
            .where(Item.logcrew == "WP", or_(Item.contact1 == username, Item.assigned1 == username))
            .order_by(Day.date.desc(), Item.itemtime.desc())
            .limit(limit)
        )
        rows = (await db.execute(stmt)).all()
        codes_map = await self._req_codes_batch(db, [item.idno for item, _ in rows])
        return [
            {"wp": mapper.work_plan_to_api(item, codes_map.get(item.idno, [])), "log_date": log_date}
            for item, log_date in rows
        ]

    async def copy_work_plan(self, db: AsyncSession, plan_id: int, target_date: date, username: str) -> dict:
        source = await self.get_work_plan(db, plan_id)
        src_item = (await db.execute(select(Item).where(Item.idno == plan_id))).scalar_one()
        day = await self._get_day_row(db, target_date)
        new_item = Item(
            dayidno=day.idno, date=target_date, day=day.day, logcrew="WP", status="Planned",
            timestamp=datetime.now(),
        )
        self._apply_wp(new_item, source)
        new_item.realstart = None
        new_item.realend = None
        new_item.status = "Planned"
        new_item.contact1 = username or new_item.contact1
        db.add(new_item)
        await db.flush()
        codes = await self._req_codes_for_wp(db, plan_id)
        await self._set_req_codes(db, new_item.idno, source.get("req_flags"), source.get("lockout_flags"))
        await db.commit()
        await db.refresh(new_item)
        return mapper.work_plan_to_api(new_item, codes)

    # ── Log items ───────────────────────────────────────────────────────────────

    async def get_log_item(self, db: AsyncSession, item_id: int) -> dict:
        row = (await db.execute(select(Item).where(Item.idno == item_id))).scalar_one_or_none()
        if not row or mapper.is_work_plan(row):
            raise HTTPException(status_code=404, detail="Log item not found")
        return mapper.log_item_to_api(row)

    async def create_log_item(self, db: AsyncSession, log_date: date, data: dict[str, Any]) -> dict:
        day = await self._get_day_row(db, log_date)
        wp_id = data.get("work_plan_id")
        if wp_id is not None:
            wp = (await db.execute(select(Item).where(Item.idno == wp_id, Item.dayidno == day.idno, Item.logcrew == "WP"))).scalar_one_or_none()
            if not wp:
                raise HTTPException(status_code=400, detail="work_plan_id must reference a work plan for this day")
        now = datetime.now()
        item = Item(
            dayidno=day.idno, date=log_date, day=day.day,
            logcrew=data.get("crew_tab", "ALL"),
            itemtime=data.get("item_time"),
            itemtitle=_strip_nul(data.get("title")),
            itemtext=_strip_nul(data.get("body")),
            type=data.get("item_type"),
            downtime=data.get("downtime_minutes"),
            subsystem=data.get("subsystem"),
            status=data.get("status"),
            user=data.get("created_by"),
            history=_strip_nul(data.get("history_text")),
            comment=_strip_nul(data.get("comment_text")),
            residno=wp_id,
            timestamp=now,
            updatestamp=now,
        )
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return mapper.log_item_to_api(item)

    async def update_log_item(self, db: AsyncSession, item_id: int, data: dict[str, Any], username: str = "system") -> dict:
        item = (await db.execute(select(Item).where(Item.idno == item_id))).scalar_one_or_none()
        if not item or mapper.is_work_plan(item):
            raise HTTPException(status_code=404, detail="Log item not found")
        if "work_plan_id" in data:
            wp_id = data["work_plan_id"]
            item.residno = wp_id
        if "crew_tab" in data and data["crew_tab"] is not None:
            item.logcrew = data["crew_tab"]
        if "item_time" in data:
            item.itemtime = data["item_time"]
        if "item_type" in data:
            item.type = data["item_type"]
        if "downtime_minutes" in data:
            item.downtime = data["downtime_minutes"]
        if "subsystem" in data:
            item.subsystem = data["subsystem"]
        if "status" in data:
            item.status = data["status"]
        if "created_by" in data:
            item.user = data["created_by"]
        if "title" in data:
            item.itemtitle = _strip_nul(data["title"])
        if "body" in data:
            item.itemtext = _strip_nul(data["body"])
        if "comment_text" in data:
            item.comment = _strip_nul(data["comment_text"])
        if "history_text" in data and data["history_text"] is not None:
            item.history = _strip_nul(data["history_text"])
        elif "title" in data or "body" in data:
            now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            title_preview = (data.get("title") or item.itemtitle or "")[:80]
            new_line = f"[{now_str}] ({username}): {title_preview}"
            existing = (item.history or "").rstrip()
            item.history = f"{existing}\n{new_line}".strip()
        item.updatestamp = datetime.now()
        await db.commit()
        await db.refresh(item)
        return mapper.log_item_to_api(item)

    async def delete_log_item(self, db: AsyncSession, item_id: int) -> None:
        await self.get_log_item(db, item_id)
        await db.execute(delete(Item).where(Item.idno == item_id))
        await db.commit()

    # ── Email ───────────────────────────────────────────────────────────────────

    async def send_summit_email(self, db: AsyncSession, log_date: date, email_type: str, username: str) -> dict:
        from app.core.config import settings

        payload = await self.get_daily_view(db=db, log_date=log_date)
        day_data = {
            "crew_assignments": payload.get("crew") or [],
            "weather": payload.get("weather"),
            "programs": payload.get("programs") or [],
            "work_plans": payload.get("work_plans") or [],
            "log_items": payload.get("log_items") or [],
        }
        body_text = self._build_email_body(log_date, day_data, email_type)
        date_str = log_date.strftime("%Y-%m-%d")

        if email_type == "smoka":
            subject = f"SMOKA Archive Log — {date_str} (from OPAL)"
            raw_recipients = settings.email_smoka_recipients
        elif email_type == "dc":
            subject = f"SciOps Day Crew Log — {date_str} (from OPAL)"
            raw_recipients = settings.email_dc_recipients
        else:
            subject = f"SciOps Night Log — {date_str} (from OPAL)"
            raw_recipients = settings.email_summitlog_recipients

        recipients = [r.strip() for r in raw_recipients.split(",") if r.strip()]
        if not recipients:
            raise HTTPException(status_code=400, detail="No email recipients configured")

        msg = MIMEText(body_text, "plain", "utf-8")
        msg["From"] = settings.email_sender
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject

        def _send_blocking() -> Optional[str]:
            try:
                with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as server:
                    server.sendmail(settings.email_sender, recipients, msg.as_string())
                return None
            except Exception as exc:
                return str(exc)

        last_error = await asyncio.get_event_loop().run_in_executor(None, _send_blocking)
        day = await self._get_day_row(db, log_date)
        now = datetime.now()
        if last_error is None:
            if email_type == "smoka":
                day.mailsmoka = "Y"
                day.smokatime = now
            elif email_type == "dc":
                day.mailday = "Y"
                day.maildtime = now
            else:
                day.mailed = "Y"
                day.mailtime = now
        await db.commit()
        if last_error:
            raise HTTPException(status_code=502, detail=f"SMTP error: {last_error}")
        return {"message": f"Email sent to {', '.join(recipients)}", "recipients": recipients}

    def _build_email_body(self, log_date: date, day_data: dict, email_type: str) -> str:
        lines = [f"Subaru SciOps Night Log — {log_date.strftime('%Y-%m-%d')}", "=" * 50]
        lines.append("\n=== CREW ===")
        for c in day_data.get("crew_assignments", []):
            lines.append(f"  {c.get('role')}: {c.get('member_name')}")
        w = day_data.get("weather")
        if w:
            lines.append("\n=== WEATHER ===")
            lines.append(f"  Sky: {w.get('sky')} | Temp: {w.get('temp_raw')}")
        if day_data.get("programs"):
            lines.append("\n=== PROGRAMS ===")
            for p in day_data["programs"]:
                lines.append(f"  {p.get('instr')} [{p.get('alloc')}]")
        if email_type == "dc" and day_data.get("work_plans"):
            lines.append("\n=== WORK PLANS ===")
            for wp in day_data["work_plans"]:
                lines.append(f"  {wp.get('comptitle') or wp.get('plan_text')}")
        if day_data.get("log_items"):
            lines.append("\n=== LOG ENTRIES ===")
            for item in day_data["log_items"]:
                lines.append(f"  [{item.get('crew_tab')}] {item.get('title')}")
        lines.append("\n— Sent from OPAL —")
        return "\n".join(lines)

    # ── Search ──────────────────────────────────────────────────────────────────

    async def search_log_items(
        self,
        db: AsyncSession,
        *,
        q: str,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        crew_tab: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[dict], int]:
        from sqlalchemy import text as sql_text
        qt = q.strip()
        if not qt:
            raise HTTPException(status_code=400, detail="Query q must not be empty")

        # Use FULLTEXT index (MATCH AGAINST) when available — falls back to LIKE for
        # short single-char queries that FULLTEXT doesn't support.
        use_fulltext = len(qt) >= 3 and not any(c in qt for c in "%_\\")

        date_clause = ""
        params: dict = {"qt": qt, "limit": limit, "offset": offset}
        if from_date:
            date_clause += " AND i.date >= :from_date"
            params["from_date"] = from_date
        if to_date:
            date_clause += " AND i.date <= :to_date"
            params["to_date"] = to_date
        crew_clause = ""
        if crew_tab:
            crew_clause = " AND i.logcrew = :crew_tab"
            params["crew_tab"] = crew_tab.strip().upper()

        if use_fulltext:
            # Boolean mode: wrap multi-word queries so each word is required (+word)
            words = qt.split()
            ft_query = " ".join(f"+{w}*" for w in words if len(w) >= 3) or qt
            params["ft_query"] = ft_query
            text_filter = "MATCH(i.itemtitle, i.itemtext) AGAINST (:ft_query IN BOOLEAN MODE)"
        else:
            esc = qt.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            params["pat"] = f"%{esc}%"
            text_filter = "(i.itemtitle LIKE :pat OR i.itemtext LIKE :pat)"

        count_sql = sql_text(
            f"SELECT COUNT(*) FROM items i WHERE {text_filter}"
            f" AND i.logcrew != 'WP'{date_clause}{crew_clause}"
        )
        rows_sql = sql_text(
            f"SELECT i.idno FROM items i WHERE {text_filter}"
            f" AND i.logcrew != 'WP'{date_clause}{crew_clause}"
            f" ORDER BY i.date DESC, i.itemtime DESC, i.idno DESC"
            f" LIMIT :limit OFFSET :offset"
        )

        total = (await db.execute(count_sql, params)).scalar_one()
        id_rows = (await db.execute(rows_sql, params)).fetchall()
        if not id_rows:
            return [], int(total)

        item_ids = [r[0] for r in id_rows]
        items = (await db.execute(
            select(Item).where(Item.idno.in_(item_ids))
            .order_by(Item.date.desc(), Item.itemtime.desc(), Item.idno.desc())
        )).scalars().all()
        return [{"item": mapper.log_item_to_api(item), "log_date": item.date} for item in items], int(total)
