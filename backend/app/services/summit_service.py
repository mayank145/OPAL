"""
Business logic for Summit Logging — full CRUD for all entities.
"""
from __future__ import annotations

import re
import uuid
from datetime import date, datetime, timezone
from typing import Any, List, Optional, Tuple
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import delete, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    CrewAssignment,
    EmailDelivery,
    LogItem,
    ObservationProgram,
    SummitDay,
    WeatherSnapshot,
    WorkPlan,
)


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

    # ── Summit Days ─────────────────────────────────────────────────────────────

    async def get_monthly_days(
        self, db: AsyncSession, year: int, month: int
    ) -> List[dict]:
        """Return day summaries for a month, including entry count and downtime totals."""
        start_date = date(year, month, 1)
        end_date = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)

        days_stmt = (
            select(SummitDay)
            .where(SummitDay.log_date >= start_date, SummitDay.log_date < end_date)
            .order_by(SummitDay.log_date.asc())
        )
        days = list((await db.execute(days_stmt)).scalars().all())
        if not days:
            return []

        day_ids = [d.id for d in days]

        counts_stmt = (
            select(
                LogItem.summit_day_id,
                func.count(LogItem.id).label("entry_count"),
                func.coalesce(func.sum(LogItem.downtime_minutes), 0).label("total_downtime"),
            )
            .where(LogItem.summit_day_id.in_(day_ids))
            .group_by(LogItem.summit_day_id)
        )
        counts_rows = (await db.execute(counts_stmt)).all()
        counts_map = {str(r.summit_day_id): (r.entry_count, r.total_downtime) for r in counts_rows}

        result = []
        for d in days:
            ec, dt = counts_map.get(str(d.id), (0, 0))
            result.append({"day": d, "entry_count": ec, "total_downtime": dt})
        return result

    async def get_yearly_days(self, db: AsyncSession, year: int) -> List[dict]:
        """Year overview: day summaries plus first program instrument per day (legacy loglist style)."""
        start_date = date(year, 1, 1)
        end_date = date(year + 1, 1, 1)
        days_stmt = (
            select(SummitDay)
            .where(SummitDay.log_date >= start_date, SummitDay.log_date < end_date)
            .order_by(SummitDay.log_date.asc())
        )
        days = list((await db.execute(days_stmt)).scalars().all())
        if not days:
            return []

        day_ids = [d.id for d in days]

        counts_stmt = (
            select(
                LogItem.summit_day_id,
                func.count(LogItem.id).label("entry_count"),
                func.coalesce(func.sum(LogItem.downtime_minutes), 0).label("total_downtime"),
            )
            .where(LogItem.summit_day_id.in_(day_ids))
            .group_by(LogItem.summit_day_id)
        )
        counts_rows = (await db.execute(counts_stmt)).all()
        counts_map = {str(r.summit_day_id): (r.entry_count, r.total_downtime) for r in counts_rows}

        prog_stmt = (
            select(ObservationProgram.summit_day_id, ObservationProgram.instr, ObservationProgram.sort_order)
            .where(ObservationProgram.summit_day_id.in_(day_ids))
            .order_by(ObservationProgram.summit_day_id, ObservationProgram.sort_order.asc())
        )
        first_instr: dict[str, str] = {}
        for row in (await db.execute(prog_stmt)).all():
            sid = str(row.summit_day_id)
            if sid not in first_instr and row.instr:
                first_instr[sid] = row.instr.strip()

        result = []
        for d in days:
            ec, dt = counts_map.get(str(d.id), (0, 0))
            result.append({
                "day": d,
                "entry_count": ec,
                "total_downtime": int(dt) if dt is not None else 0,
                "first_instr": first_instr.get(str(d.id)),
            })
        return result

    async def create_summit_day(self, db: AsyncSession, log_date: date, day_label: Optional[str], history_text: Optional[str]) -> SummitDay:
        existing = await db.execute(select(SummitDay).where(SummitDay.log_date == log_date))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=409, detail=f"Summit day already exists for {log_date}")
        now = datetime.now(timezone.utc)
        day = SummitDay(
            id=uuid.uuid4(),
            log_date=log_date,
            day_label=_strip_nul(day_label),
            history_text=_strip_nul(history_text),
            created_at=now,
            updated_at=now,
        )
        db.add(day)
        await db.commit()
        await db.refresh(day)
        return day

    async def get_daily_view(self, db: AsyncSession, log_date: date) -> dict:
        day = await self._get_day_header(db, log_date)
        crew = await self._get_crew_assignments(db, day.id)
        weather = await self._get_weather(db, day.id)
        programs = await self._get_programs(db, day.id)
        work_plans = await self._get_work_plans(db, day.id)
        log_items = await self._get_log_items(db, day.id)
        email_delivery = await self._get_email_delivery(db, day.id)

        entry_count = len(log_items)
        total_downtime = sum((li.downtime_minutes or 0) for li in log_items)

        return {
            "day": day,
            "crew": crew,
            "weather": weather,
            "programs": programs,
            "work_plans": work_plans,
            "log_items": log_items,
            "email_delivery": email_delivery,
            "entry_count": entry_count,
            "total_downtime": total_downtime,
        }

    async def update_summit_day(self, db: AsyncSession, log_date: date, data: dict[str, Any]) -> SummitDay:
        day = await self._get_day_header(db, log_date)
        if "day_label" in data:
            day.day_label = _strip_nul(data["day_label"])
        if "history_text" in data:
            day.history_text = _strip_nul(data["history_text"])
        if "zoom_meeting_id" in data:
            day.zoom_meeting_id = _strip_nul(data["zoom_meeting_id"])
        if "zoom_password" in data:
            day.zoom_password = _strip_nul(data["zoom_password"])
        if "zoom_join_url" in data:
            day.zoom_join_url = _strip_nul(data["zoom_join_url"])
        day.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(day)
        return day

    async def get_summit_day_by_date(self, db: AsyncSession, log_date: date) -> SummitDay:
        return await self._get_day_header(db, log_date)

    async def _get_day_header(self, db: AsyncSession, log_date: date) -> SummitDay:
        result = await db.execute(select(SummitDay).where(SummitDay.log_date == log_date))
        day = result.scalar_one_or_none()
        if not day:
            raise HTTPException(status_code=404, detail=f"Summit day not found for {log_date}")
        return day

    # ── Crew Assignments ────────────────────────────────────────────────────────

    async def _get_crew_assignments(self, db: AsyncSession, summit_day_id) -> List[CrewAssignment]:
        stmt = (
            select(CrewAssignment)
            .where(CrewAssignment.summit_day_id == summit_day_id)
            .order_by(CrewAssignment.sort_order.asc(), CrewAssignment.id.asc())
        )
        return list((await db.execute(stmt)).scalars().all())

    async def get_crew(self, db: AsyncSession, crew_id: UUID) -> CrewAssignment:
        row = (await db.execute(select(CrewAssignment).where(CrewAssignment.id == crew_id))).scalar_one_or_none()
        if not row:
            raise HTTPException(status_code=404, detail="Crew assignment not found")
        return row

    async def create_crew(self, db: AsyncSession, log_date: date, data: dict[str, Any]) -> CrewAssignment:
        day = await self._get_day_header(db, log_date)
        if data.get("sort_order") is None:
            mx = (await db.execute(
                select(func.max(CrewAssignment.sort_order)).where(CrewAssignment.summit_day_id == day.id)
            )).scalar_one()
            sort_order = (mx or 0) + 1
        else:
            sort_order = int(data["sort_order"])

        row = CrewAssignment(
            id=uuid.uuid4(),
            summit_day_id=day.id,
            role=data["role"],
            member_name=_strip_nul(data.get("member_name")),
            location=_strip_nul(data.get("location")),
            time_in=data.get("time_in"),
            time_out=data.get("time_out"),
            sort_order=sort_order,
        )
        db.add(row)
        await db.commit()
        await db.refresh(row)
        return row

    async def update_crew(self, db: AsyncSession, crew_id: UUID, data: dict[str, Any]) -> CrewAssignment:
        row = await self.get_crew(db, crew_id)
        for field in ("role", "member_name", "location", "time_in", "time_out", "sort_order"):
            if field in data and data[field] is not None:
                val = _strip_nul(data[field]) if field in ("member_name", "location") else data[field]
                setattr(row, field, val)
        await db.commit()
        await db.refresh(row)
        return row

    async def delete_crew(self, db: AsyncSession, crew_id: UUID) -> None:
        await self.get_crew(db, crew_id)
        await db.execute(delete(CrewAssignment).where(CrewAssignment.id == crew_id))
        await db.commit()

    # ── Weather Snapshots ───────────────────────────────────────────────────────

    async def _get_weather(self, db: AsyncSession, summit_day_id) -> Optional[WeatherSnapshot]:
        return (await db.execute(select(WeatherSnapshot).where(WeatherSnapshot.summit_day_id == summit_day_id))).scalar_one_or_none()

    async def upsert_weather(self, db: AsyncSession, log_date: date, data: dict[str, Any]) -> WeatherSnapshot:
        day = await self._get_day_header(db, log_date)
        snap = await self._get_weather(db, day.id)
        if snap is None:
            snap = WeatherSnapshot(id=uuid.uuid4(), summit_day_id=day.id)
            db.add(snap)

        for field in ("sky", "seeing", "wind", "comment_text"):
            if field in data:
                setattr(snap, field, _strip_nul(data[field]))

        if "temp_raw" in data:
            snap.temp_raw = _strip_nul(data["temp_raw"])
            snap.temp_c = _parse_float(data["temp_raw"])
        if "humidity_raw" in data:
            snap.humidity_raw = _strip_nul(data["humidity_raw"])
            snap.humidity_pct = _parse_float(data["humidity_raw"])
        if "captured_at" in data:
            snap.captured_at = data["captured_at"]

        await db.commit()
        await db.refresh(snap)
        return snap

    # ── Observation Programs ────────────────────────────────────────────────────

    async def _get_programs(self, db: AsyncSession, summit_day_id) -> List[ObservationProgram]:
        stmt = (
            select(ObservationProgram)
            .where(ObservationProgram.summit_day_id == summit_day_id)
            .order_by(ObservationProgram.sort_order.asc(), ObservationProgram.id.asc())
        )
        return list((await db.execute(stmt)).scalars().all())

    async def get_program(self, db: AsyncSession, program_id: UUID) -> ObservationProgram:
        row = (await db.execute(select(ObservationProgram).where(ObservationProgram.id == program_id))).scalar_one_or_none()
        if not row:
            raise HTTPException(status_code=404, detail="Program not found")
        return row

    def _apply_program_data(self, p: ObservationProgram, data: dict[str, Any]) -> None:
        str_fields = (
            "instr", "alloc", "pi", "ao1", "ao2", "gid", "propid",
            "obs1", "obs1loc", "obs2", "obs2loc", "obs3", "obs3loc", "obs4", "obs4loc",
            "ss", "ssloc", "ss2", "ss2loc",
            "others1", "others1loc", "others2", "others2loc",
            "notes", "comment_text",
        )
        for f in str_fields:
            if f in data:
                setattr(p, f, _strip_nul(data[f]))
        for f in ("slot_start", "slot_end"):
            if f in data:
                setattr(p, f, data[f])
        if "sort_order" in data and data["sort_order"] is not None:
            p.sort_order = int(data["sort_order"])
        p.program_code = _strip_nul(p.gid or p.propid)

    async def create_program(self, db: AsyncSession, log_date: date, data: dict[str, Any]) -> ObservationProgram:
        day = await self._get_day_header(db, log_date)
        if data.get("sort_order") is None:
            mx = (await db.execute(
                select(func.max(ObservationProgram.sort_order)).where(ObservationProgram.summit_day_id == day.id)
            )).scalar_one()
            data = {**data, "sort_order": (mx or 0) + 1}

        p = ObservationProgram(id=uuid.uuid4(), legacy_prog_id=None, summit_day_id=day.id, sort_order=0)
        self._apply_program_data(p, data)
        db.add(p)
        await db.commit()
        await db.refresh(p)
        return p

    async def update_program(self, db: AsyncSession, program_id: UUID, data: dict[str, Any]) -> ObservationProgram:
        p = await self.get_program(db, program_id)
        self._apply_program_data(p, data)
        await db.commit()
        await db.refresh(p)
        return p

    async def delete_program(self, db: AsyncSession, program_id: UUID) -> None:
        await self.get_program(db, program_id)
        await db.execute(delete(ObservationProgram).where(ObservationProgram.id == program_id))
        await db.commit()

    # ── Work Plans ──────────────────────────────────────────────────────────────

    async def _get_work_plans(self, db: AsyncSession, summit_day_id) -> List[WorkPlan]:
        stmt = (
            select(WorkPlan)
            .where(WorkPlan.summit_day_id == summit_day_id)
            .order_by(WorkPlan.window_start.asc().nulls_last(), WorkPlan.id.asc())
        )
        return list((await db.execute(stmt)).scalars().all())

    async def get_work_plan(self, db: AsyncSession, plan_id: UUID) -> WorkPlan:
        row = (await db.execute(select(WorkPlan).where(WorkPlan.id == plan_id))).scalar_one_or_none()
        if not row:
            raise HTTPException(status_code=404, detail="Work plan not found")
        return row

    _WP_STR_FIELDS = (
        "nite_effect", "day_effect",
        "location", "location2", "location3",
        "assigned1", "assigned2", "dcassist", "notify",
        "contact1", "contact2", "others", "otherreq",
        "comptitle", "comptext", "requirements", "notes",
        "intervene", "melco", "fai", "pass_text", "rpass_text",
    )

    def _apply_wp_data(self, wp: WorkPlan, data: dict[str, Any]) -> None:
        for f in self._WP_STR_FIELDS:
            if f in data:
                setattr(wp, f, _strip_nul(data[f]))
        for f in ("window_start", "window_end"):
            if f in data:
                setattr(wp, f, data[f])
        for f in ("master", "seats", "seats2", "pseats"):
            if f in data and data[f] is not None:
                setattr(wp, f, int(data[f]))
            elif f in data and data[f] is None:
                setattr(wp, f, None)

    async def create_work_plan(self, db: AsyncSession, log_date: date, data: dict[str, Any]) -> WorkPlan:
        day = await self._get_day_header(db, log_date)
        wp = WorkPlan(id=uuid.uuid4(), summit_day_id=day.id)
        self._apply_wp_data(wp, data)
        db.add(wp)
        await db.commit()
        await db.refresh(wp)
        return wp

    async def update_work_plan(self, db: AsyncSession, plan_id: UUID, data: dict[str, Any]) -> WorkPlan:
        wp = await self.get_work_plan(db, plan_id)
        self._apply_wp_data(wp, data)
        await db.commit()
        await db.refresh(wp)
        return wp

    async def delete_work_plan(self, db: AsyncSession, plan_id: UUID) -> None:
        await self.get_work_plan(db, plan_id)
        await db.execute(delete(WorkPlan).where(WorkPlan.id == plan_id))
        await db.commit()

    # ── Log Items ───────────────────────────────────────────────────────────────

    async def _get_log_items(self, db: AsyncSession, summit_day_id) -> List[LogItem]:
        stmt = (
            select(LogItem)
            .where(LogItem.summit_day_id == summit_day_id)
            .order_by(LogItem.item_time.asc().nulls_last(), LogItem.id.asc())
        )
        return list((await db.execute(stmt)).scalars().all())

    async def get_log_item(self, db: AsyncSession, item_id: UUID) -> LogItem:
        row = (await db.execute(select(LogItem).where(LogItem.id == item_id))).scalar_one_or_none()
        if not row:
            raise HTTPException(status_code=404, detail="Log item not found")
        return row

    async def create_log_item(self, db: AsyncSession, log_date: date, data: dict[str, Any]) -> LogItem:
        day = await self._get_day_header(db, log_date)
        wp_id = data.get("work_plan_id")
        if wp_id is not None:
            if not (await db.execute(select(WorkPlan).where(WorkPlan.id == wp_id, WorkPlan.summit_day_id == day.id))).scalar_one_or_none():
                raise HTTPException(status_code=400, detail="work_plan_id must reference a work plan for this summit day")

        now = datetime.now(timezone.utc)
        item = LogItem(
            id=uuid.uuid4(),
            summit_day_id=day.id,
            work_plan_id=wp_id,
            legacy_item_id=None,
            legacy_old_item_id=None,
            crew_tab=data.get("crew_tab", "ALL"),
            item_time=data.get("item_time"),
            title=_strip_nul(data.get("title")),
            body=_strip_nul(data.get("body")),
            item_type=data.get("item_type"),
            downtime_minutes=data.get("downtime_minutes"),
            subsystem=data.get("subsystem"),
            status=data.get("status"),
            created_by=data.get("created_by"),
            history_text=_strip_nul(data.get("history_text")),
            comment_text=_strip_nul(data.get("comment_text")),
            summit_access=_strip_nul(data.get("summit_access")),
            created_at=now,
            updated_at=now,
        )
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    async def update_log_item(self, db: AsyncSession, item_id: UUID, data: dict[str, Any]) -> LogItem:
        item = await self.get_log_item(db, item_id)
        if "work_plan_id" in data:
            wp_id = data["work_plan_id"]
            if wp_id is None:
                item.work_plan_id = None
            else:
                if not (await db.execute(select(WorkPlan).where(WorkPlan.id == wp_id, WorkPlan.summit_day_id == item.summit_day_id))).scalar_one_or_none():
                    raise HTTPException(status_code=400, detail="work_plan_id must reference a work plan for this summit day")
                item.work_plan_id = wp_id
        if "crew_tab" in data and data["crew_tab"] is not None:
            item.crew_tab = data["crew_tab"]
        for field in ("item_time", "item_type", "downtime_minutes", "subsystem", "status", "created_by"):
            if field in data:
                setattr(item, field, data[field])
        for field in ("title", "body", "history_text", "comment_text"):
            if field in data:
                setattr(item, field, _strip_nul(data[field]))
        if "summit_access" in data:
            item.summit_access = _strip_nul(data["summit_access"])
        item.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(item)
        return item

    async def delete_log_item(self, db: AsyncSession, item_id: UUID) -> None:
        await self.get_log_item(db, item_id)
        await db.execute(delete(LogItem).where(LogItem.id == item_id))
        await db.commit()

    # ── Email Delivery ──────────────────────────────────────────────────────────

    async def _get_email_delivery(self, db: AsyncSession, summit_day_id) -> Optional[EmailDelivery]:
        return (await db.execute(select(EmailDelivery).where(EmailDelivery.summit_day_id == summit_day_id))).scalar_one_or_none()

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
        qt = q.strip()
        if not qt:
            raise HTTPException(status_code=400, detail="Query q must not be empty")

        join_cond = LogItem.summit_day_id == SummitDay.id
        esc = qt.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        pat = f"%{esc}%"
        text_match = or_(
            LogItem.title.ilike(pat, escape="\\"),
            LogItem.body.ilike(pat, escape="\\"),
        )
        fts_safe = re.sub(r"[^\w\s]", " ", qt, flags=re.UNICODE)
        fts_safe = " ".join(fts_safe.split())[:500]
        if fts_safe:
            vec = func.to_tsvector(
                "english",
                func.concat_ws(" ", func.coalesce(LogItem.title, ""), func.coalesce(LogItem.body, "")),
            )
            fts_q = func.plainto_tsquery("english", fts_safe)
            keyword_clause = or_(text_match, vec.op("@@")(fts_q))
        else:
            keyword_clause = text_match

        filters: list = [keyword_clause]
        if from_date is not None:
            filters.append(SummitDay.log_date >= from_date)
        if to_date is not None:
            filters.append(SummitDay.log_date <= to_date)
        if crew_tab is not None:
            filters.append(LogItem.crew_tab == crew_tab.strip().upper())

        count_stmt = (
            select(func.count())
            .select_from(LogItem)
            .join(SummitDay, join_cond)
            .where(*filters)
        )
        total = (await db.execute(count_stmt)).scalar_one()

        stmt = (
            select(LogItem, SummitDay.log_date)
            .join(SummitDay, join_cond)
            .where(*filters)
            .order_by(SummitDay.log_date.desc(), LogItem.item_time.desc().nulls_last(), LogItem.id.desc())
            .limit(limit)
            .offset(offset)
        )
        rows = (await db.execute(stmt)).all()
        result = []
        for item, log_date in rows:
            result.append({"item": item, "log_date": log_date})
        return result, int(total)
