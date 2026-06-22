"""
Map legacy sumlogs rows ↔ modern Summit API response shapes.
"""
from __future__ import annotations

import html
from datetime import date, datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Set

from app.models.summit_legacy import Day, Item, Prog

# Legacy sumlogs stores all datetimes as naive HST (UTC-10). Tag them so
# browsers in other timezones can display them correctly.
_HST = timezone(timedelta(hours=-10))

LOCKOUT_FLAG_SET = {
    "No-Tel-Move", "No-AZ-Move", "No-EL-Move", "NoLights-Dome",
    "No-TopScreen-Move", "No-MirrorCover-Move", "No-MainShutter", "No-UnitSelector-Move",
}

CREW_SLOTS = [
    {"id": "TO1", "role": "TO", "name": "to1", "loc": "to1loc", "tin": "toin", "tout": "toout", "sort": 0},
    {"id": "TO2", "role": "TO", "name": "to2", "loc": None, "tin": None, "tout": None, "sort": 1},
    {"id": "IO1", "role": "IO", "name": "io1", "loc": "io1loc", "tin": "ioin", "tout": "ioout", "sort": 2},
    {"id": "IO2", "role": "IO", "name": "io2", "loc": None, "tin": None, "tout": None, "sort": 3},
    {"id": "DC1", "role": "DC", "name": "dc1", "loc": None, "tin": "dcin", "tout": "dcout", "sort": 4},
    {"id": "DC2", "role": "DC", "name": "dc2", "loc": None, "tin": None, "tout": None, "sort": 5},
]

CREW_SLOT_BY_ID = {s["id"]: s for s in CREW_SLOTS}


def _clean_datetime(v: Any) -> Optional[datetime]:
    """Return v as a timezone-aware datetime tagged as HST (-10:00).
    Naive datetimes from the legacy DB are assumed to be stored in HST.
    """
    if v is None:
        return None
    if isinstance(v, str) and v.startswith("0000-00-00"):
        return None
    if isinstance(v, datetime):
        if v.year == 0 or v.month == 0 or v.day == 0:
            return None
        # Tag naive datetimes as HST so clients in all timezones display correctly
        if v.tzinfo is None:
            return v.replace(tzinfo=_HST)
        return v
    return v


def _clean_text(v: Any) -> Optional[str]:
    """Decode HTML entities from legacy data (e.g. &quot; → \")."""
    if v is None:
        return None
    s = str(v)
    return html.unescape(s) if "&" in s else s


def _parse_int(v: Any) -> int:
    if v is None or v == "":
        return 0
    try:
        return int(str(v).strip())
    except (ValueError, TypeError):
        return 0


def _parse_float(s: Any) -> Optional[float]:
    if s is None or s == "":
        return None
    try:
        return float(str(s).strip())
    except (ValueError, TypeError):
        return None


def _seq_order(seq: Optional[str]) -> int:
    if not seq:
        return 0
    s = str(seq).strip()
    if len(s) == 1 and s.isalpha():
        return ord(s.upper()) - ord("A")
    try:
        return int(s)
    except ValueError:
        return 0


def day_to_api(day: Day) -> Dict[str, Any]:
    return {
        "id": day.idno,
        "log_date": day.date,
        "day_label": _clean_text(day.day),
        "history_text": _clean_text(day.history),
        "zoom_meeting_id": None,
        "zoom_password": None,
        "zoom_join_url": None,
    }


def crew_from_day(day: Day) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for slot in CREW_SLOTS:
        name = getattr(day, slot["name"], None)
        if not name or not str(name).strip():
            continue
        rows.append({
            "id": slot["id"],
            "summit_day_id": day.idno,
            "role": slot["role"],
            "member_name": str(name).strip(),
            "location": (getattr(day, slot["loc"], None) or None) if slot["loc"] else None,
            "time_in": _clean_datetime(getattr(day, slot["tin"], None) if slot["tin"] else None),
            "time_out": _clean_datetime(getattr(day, slot["tout"], None) if slot["tout"] else None),
            "sort_order": slot["sort"],
        })
    return rows


def weather_from_day(day: Day) -> Optional[Dict[str, Any]]:
    if not any(getattr(day, f, None) for f in ("sky", "seeing", "temp", "wind", "humid", "comment")):
        return None
    return {
        "id": day.idno,
        "sky": day.sky,
        "seeing": day.seeing,
        "temp_raw": day.temp,
        "temp_c": _parse_float(day.temp),
        "wind": day.wind,
        "humidity_raw": day.humid,
        "humidity_pct": _parse_float(day.humid),
        "comment_text": day.comment,
        "captured_at": None,
    }


def email_from_day(day: Day) -> Optional[Dict[str, Any]]:
    if not any(getattr(day, f, None) for f in ("mailed", "mailsmoka", "mailday")):
        return None
    return {
        "id": day.idno,
        "mailed": day.mailed,
        "mailtime": _clean_datetime(day.mailtime),
        "mailsmoka": day.mailsmoka,
        "smokatime": _clean_datetime(day.smokatime),
        "mailday": day.mailday,
        "maildtime": _clean_datetime(day.maildtime),
        "am_sent_at": None,
        "pm_sent_at": _clean_datetime(day.mailtime),
        "day_digest_sent_at": _clean_datetime(day.maildtime),
        "last_error": None,
    }


def prog_to_api(prog: Prog) -> Dict[str, Any]:
    return {
        "id": prog.idno,
        "legacy_prog_id": prog.idno,
        "summit_day_id": prog.dayidno,
        "sort_order": _seq_order(prog.seq),
        "program_code": prog.gid or prog.propid,
        "instr": _clean_text(prog.instr),
        "alloc": _clean_text(prog.alloc),
        "pi": _clean_text(prog.pi),
        "ao1": _clean_text(prog.ao1),
        "ao2": _clean_text(prog.ao2),
        "slot_start": _clean_datetime(prog.intime),
        "slot_end": _clean_datetime(prog.outtime),
        "gid": prog.gid,
        "propid": prog.propid,
        "obs1": prog.obs1,
        "obs1loc": prog.obs1loc,
        "obs2": prog.obs2,
        "obs2loc": prog.obs2loc,
        "obs3": prog.obs3,
        "obs3loc": prog.obs3loc,
        "obs4": prog.obs4,
        "obs4loc": prog.obs4loc,
        "ss": prog.ss,
        "ssloc": prog.ssloc,
        "ss2": prog.ss2,
        "ss2loc": prog.ss2loc,
        "others1": prog.others1,
        "others1loc": prog.others1loc,
        "others2": prog.others2,
        "others2loc": prog.others2loc,
        "notes": None,
        "comment_text": prog.comment,
    }


def _item_req_flags(req_codes: List[str]) -> tuple[Optional[str], Optional[str]]:
    req, lock = [], []
    for code in req_codes:
        if code in LOCKOUT_FLAG_SET:
            lock.append(code)
        else:
            req.append(code)
    return (",".join(req) or None, ",".join(lock) or None)


def work_plan_to_api(item: Item, req_codes: Optional[List[str]] = None) -> Dict[str, Any]:
    req_f, lock_f = _item_req_flags(req_codes or [])
    return {
        "id": item.idno,
        "summit_day_id": item.dayidno,
        "requestor": item.contact1,
        "wp_status": item.status or "Planned",
        "wp_type": item.type,
        "wp_subsystem": item.subsystem,
        "plan_text": item.itemtext,
        "day_warning": item.comment,
        "nite_warning": None,
        "teampass": item.pass_,
        "realstart": _clean_datetime(item.realstart),
        "realend": _clean_datetime(item.realend),
        "req_flags": req_f,
        "lockout_flags": lock_f,
        "window_start": _clean_datetime(item.itemtime),
        "window_end": _clean_datetime(item.endtime),
        "nite_effect": item.niteeffect,
        "day_effect": item.dayeffect,
        "location": item.location,
        "location2": item.location2,
        "location3": item.location3,
        "assigned1": item.assigned1,
        "assigned2": item.assigned2,
        "dcassist": item.dcassist,
        "notify": item.notify,
        "contact1": item.contact1,
        "contact2": item.contact2,
        "others": item.others,
        "otherreq": item.otherreq,
        "comptitle": item.comptitle,
        "comptext": item.comptext,
        "completion_title": None,
        "intervene": item.intervene,
        "melco": item.melco,
        "fai": item.fai,
        "master": item.master,
        "seats": item.seats,
        "seats2": item.seats2,
        "pseats": item.pseats,
        "pass_text": item.pass_,
        "rpass_text": item.rpass,
        "requirements": item.otherreq,
        "notes": item.itemtext,
    }


def log_item_to_api(item: Item) -> Dict[str, Any]:
    wp_id = None
    for field in ("residno", "residno2", "residno3", "residno4", "residno5", "residno6"):
        val = getattr(item, field, None)
        if val:
            wp_id = val
            break
    crew = (item.logcrew or "ALL").strip().upper() or "ALL"
    return {
        "id": item.idno,
        "summit_day_id": item.dayidno,
        "work_plan_id": wp_id,
        "legacy_item_id": item.idno,
        "legacy_old_item_id": item.oldidno,
        "crew_tab": crew,
        "item_time": _clean_datetime(item.itemtime),
        "item_type": item.type,
        "subsystem": item.subsystem,
        "status": item.status,
        "title": _clean_text(item.itemtitle),
        "body": _clean_text(item.itemtext),
        "downtime_minutes": _parse_int(item.downtime),
        "created_by": item.user,
        "history_text": _clean_text(item.history),
        "comment_text": _clean_text(item.comment),
        "summit_access": None,
        "created_at": _clean_datetime(item.timestamp),
        "updated_at": _clean_datetime(item.updatestamp),
    }


def is_work_plan(item: Item) -> bool:
    return (item.logcrew or "").strip().upper() == "WP"


def is_log_item(item: Item) -> bool:
    return not is_work_plan(item)
