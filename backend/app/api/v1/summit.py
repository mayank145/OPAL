"""
Summit Logging API — full CRUD against legacy MariaDB `sumlogs`.
"""
from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from fastapi import APIRouter, Body, Depends, Query, status
from sqlalchemy import and_, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import require_auth
from app.db.session import get_summit_db, get_legacy_clients_db
from app.models.summit_legacy import Day, Item, Prog
from app.models.legacy_clients import ClientAlloc
from app.schemas.summit import (
    CrewAssignmentCreate,
    CrewAssignmentResponse,
    CrewAssignmentUpdate,
    EmailDeliveryResponse,
    LogItemCreate,
    LogItemResponse,
    LogItemUpdate,
    LogSearchResponse,
    ObservationProgramCreate,
    ObservationProgramResponse,
    ObservationProgramUpdate,
    SummitDailyViewResponse,
    SummitDayCreate,
    SummitDayUpdate,
    SummitMonthlyDayResponse,
    WeatherSnapshotResponse,
    WeatherSnapshotUpdate,
    WorkPlanCreate,
    WorkPlanResponse,
    WorkPlanUpdate,
)
from app.services.summit_service import SummitService

router = APIRouter()
summit_service = SummitService()


def _day_response(d: dict) -> SummitMonthlyDayResponse:
    return SummitMonthlyDayResponse.model_validate(d)


def _daily_view(payload: dict) -> SummitDailyViewResponse:
    day = payload["day"]
    return SummitDailyViewResponse(
        id=day["id"],
        log_date=day["log_date"],
        day_label=day.get("day_label"),
        history_text=day.get("history_text"),
        zoom_meeting_id=day.get("zoom_meeting_id"),
        zoom_password=day.get("zoom_password"),
        zoom_join_url=day.get("zoom_join_url"),
        entry_count=payload["entry_count"],
        total_downtime=payload["total_downtime"],
        crew_assignments=[CrewAssignmentResponse.model_validate(c) for c in payload["crew"]],
        weather=WeatherSnapshotResponse.model_validate(payload["weather"]) if payload.get("weather") else None,
        programs=[ObservationProgramResponse.model_validate(p) for p in payload["programs"]],
        work_plans=[WorkPlanResponse.model_validate(wp) for wp in payload["work_plans"]],
        log_items=[LogItemResponse.model_validate(li) for li in payload["log_items"]],
        email_delivery=EmailDeliveryResponse.model_validate(payload["email_delivery"]) if payload.get("email_delivery") else None,
    )


# ── Health ──────────────────────────────────────────────────────────────────────
@router.get("/health")
async def summit_health(db: AsyncSession = Depends(get_summit_db)):
    result = await db.execute(text("SELECT 1"))
    result.scalar_one()
    return {"status": "healthy", "database": "mariadb", "schema": "sumlogs", "service": "summit-logging"}


# ── Monthly ─────────────────────────────────────────────────────────────────────
@router.get("/monthly", response_model=dict)
async def monthly(
    year: int = Query(..., ge=1900, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: AsyncSession = Depends(get_summit_db),
):
    entries = await summit_service.get_monthly_days(db=db, year=year, month=month)
    days_out = []
    for e in entries:
        d = e["day"]
        days_out.append(
            SummitMonthlyDayResponse(
                id=d["id"],
                log_date=d["log_date"],
                day_label=d.get("day_label"),
                history_text=d.get("history_text"),
                entry_count=e["entry_count"],
                total_downtime=e["total_downtime"],
                first_instr=None,
            )
        )
    return {"year": year, "month": month, "days": days_out}


@router.get("/monthly-work-plans", response_model=dict)
async def monthly_work_plans(
    year: int = Query(..., ge=1900, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: AsyncSession = Depends(get_summit_db),
):
    import calendar as _calendar

    first_day = date(year, month, 1)
    last_day = date(year, month, _calendar.monthrange(year, month)[1])

    stmt = (
        select(Item, Day.date)
        .join(Day, Item.dayidno == Day.idno)
        .where(
            and_(
                Item.logcrew == "WP",
                Day.date >= first_day,
                Day.date <= last_day,
            )
        )
        .order_by(Day.date.asc(), Item.itemtime.is_(None), Item.itemtime.asc())
    )
    rows = (await db.execute(stmt)).all()

    from app.services import summit_legacy_mapper as mapper
    wp_ids = [item.idno for item, _ in rows]
    codes_map = await summit_service._req_codes_batch(db, wp_ids)
    grouped: dict = {}
    for item, log_date in rows:
        key = str(log_date)
        grouped.setdefault(key, []).append(
            WorkPlanResponse.model_validate(
                mapper.work_plan_to_api(item, codes_map.get(item.idno, []))
            ).model_dump()
        )

    return {"year": year, "month": month, "work_plans_by_date": grouped}


@router.get("/year/{year}", response_model=dict)
async def yearly(year: int, db: AsyncSession = Depends(get_summit_db)):
    entries = await summit_service.get_yearly_days(db=db, year=year)
    days_out = []
    for e in entries:
        d = e["day"]
        days_out.append(
            SummitMonthlyDayResponse(
                id=d["id"],
                log_date=d["log_date"],
                day_label=d.get("day_label"),
                history_text=d.get("history_text"),
                entry_count=e["entry_count"],
                total_downtime=e["total_downtime"],
                first_instr=e.get("first_instr"),
            )
        )
    return {"year": year, "days": days_out}


# ── Summit Days ─────────────────────────────────────────────────────────────────
@router.post("/days", response_model=SummitMonthlyDayResponse, status_code=status.HTTP_201_CREATED)
async def create_summit_day(
    body: SummitDayCreate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    day = await summit_service.create_summit_day(db, body.log_date, body.day_label, body.history_text)
    return _day_response(day)


@router.get("/day/{log_date}", response_model=SummitDailyViewResponse)
async def day_view(log_date: date, db: AsyncSession = Depends(get_summit_db)):
    return _daily_view(await summit_service.get_daily_view(db=db, log_date=log_date))


@router.patch("/day/{log_date}", response_model=SummitMonthlyDayResponse)
async def patch_summit_day(
    log_date: date,
    body: SummitDayUpdate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    day = await summit_service.update_summit_day(db, log_date, body.model_dump(exclude_unset=True))
    return _day_response(day)


# ── Crew Assignments ────────────────────────────────────────────────────────────
@router.post("/day/{log_date}/crew", response_model=CrewAssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_crew(
    log_date: date,
    body: CrewAssignmentCreate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    row = await summit_service.create_crew(db, log_date, body.model_dump())
    return CrewAssignmentResponse.model_validate(row)


@router.patch("/crew/{crew_id}", response_model=CrewAssignmentResponse)
async def patch_crew(
    crew_id: str,
    body: CrewAssignmentUpdate,
    log_date: date = Query(..., description="Summit log date for this crew slot"),
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    row = await summit_service.update_crew_by_id(
        db, log_date, crew_id, body.model_dump(exclude_unset=True)
    )
    return CrewAssignmentResponse.model_validate(row)


@router.delete("/crew/{crew_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_crew(
    crew_id: str,
    log_date: date = Query(..., description="Summit log date for this crew slot"),
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    await summit_service.delete_crew(db, log_date, crew_id)


# ── Weather Snapshots ───────────────────────────────────────────────────────────
@router.put("/day/{log_date}/weather", response_model=WeatherSnapshotResponse)
async def upsert_weather(
    log_date: date,
    body: WeatherSnapshotUpdate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    snap = await summit_service.upsert_weather(db, log_date, body.model_dump(exclude_unset=True))
    return WeatherSnapshotResponse.model_validate(snap)


# ── OPAL Programs (nightly schedule from legacy clients.alloc) ─────────────────
@router.get("/day/{log_date}/opal-programs")
async def get_opal_programs(
    log_date: date,
    db: AsyncSession = Depends(get_legacy_clients_db),
):
    """
    Return programs scheduled for log_date from the remote legacy clients.alloc table.
    Displayed as 'OPAL Programs for {date}' with Copy-Program buttons.
    """
    result = await db.execute(
        select(ClientAlloc)
        .where(ClientAlloc.datein == log_date)
        .order_by(ClientAlloc.idno)
    )
    rows = result.scalars().all()
    return [
        {
            "alloc_id": r.idno,
            "gid": (r.gid or "").strip(),
            "propid": (r.propid or "").strip(),
            "instr": (r.instr or "").strip(),
            "pi": f"{(r.first or '').strip()} {(r.last or '').strip()}".strip(),
            "observers": (r.observers or "").strip(),
            "remote": (r.remote or "").strip(),
            "staff": (r.staff or "").strip(),
            "sem": (r.sem or "").strip(),
            "comment": (r.comment or "").strip(),
        }
        for r in rows
    ]


# ── Program Lookup (OPAL copy-in) ───────────────────────────────────────────────
@router.get("/programs/gids")
async def list_program_gids(
    q: str = Query("", description="Search prefix for GID / PropID"),
    db: AsyncSession = Depends(get_summit_db),
):
    """Return distinct GIDs/PropIDs matching the search prefix for autocomplete."""
    from sqlalchemy import func
    q_clean = q.strip()
    base = select(Prog.gid, Prog.propid, Prog.instr, Prog.alloc, Prog.pi).where(
        Prog.gid.isnot(None), Prog.gid != ""
    )
    if q_clean:
        like = f"{q_clean}%"
        base = base.where(or_(Prog.gid.ilike(like), Prog.propid.ilike(like)))
    base = base.order_by(Prog.dayidno.desc()).limit(200)
    rows = (await db.execute(base)).mappings().all()
    seen: dict = {}
    for r in rows:
        key = (r["gid"] or "").strip()
        if key and key not in seen:
            seen[key] = {
                "gid": key,
                "propid": (r["propid"] or "").strip(),
                "instr": (r["instr"] or "").strip(),
                "alloc": (r["alloc"] or "").strip(),
                "pi": (r["pi"] or "").strip(),
            }
        if len(seen) >= 50:
            break
    return list(seen.values())


@router.get("/programs/lookup")
async def lookup_program_by_gid(
    gid: str = Query(..., description="GID or PropID to look up"),
    db: AsyncSession = Depends(get_summit_db),
):
    """Return the most recent program entry for a GID/PropID to auto-fill the form."""
    from app.services import summit_legacy_mapper as mapper
    result = await db.execute(
        select(Prog)
        .where(or_(Prog.gid == gid, Prog.propid == gid))
        .order_by(Prog.dayidno.desc())
        .limit(1)
    )
    prog = result.scalar_one_or_none()
    if not prog:
        return {}
    return mapper.prog_to_api(prog)


# ── Observation Programs ────────────────────────────────────────────────────────
@router.post("/day/{log_date}/programs", response_model=ObservationProgramResponse, status_code=status.HTTP_201_CREATED)
async def create_program(
    log_date: date,
    body: ObservationProgramCreate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    p = await summit_service.create_program(db, log_date, body.model_dump(exclude_unset=True))
    return ObservationProgramResponse.model_validate(p)


@router.patch("/programs/{program_id}", response_model=ObservationProgramResponse)
async def patch_program(
    program_id: int,
    body: ObservationProgramUpdate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    p = await summit_service.update_program(db, program_id, body.model_dump(exclude_unset=True))
    return ObservationProgramResponse.model_validate(p)


@router.delete("/programs/{program_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_program(
    program_id: int,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    await summit_service.delete_program(db, program_id)


# ── Work Plans ──────────────────────────────────────────────────────────────────
@router.post("/day/{log_date}/work-plans", response_model=WorkPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_work_plan(
    log_date: date,
    body: WorkPlanCreate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    wp = await summit_service.create_work_plan(db, log_date, body.model_dump(exclude_unset=True))
    return WorkPlanResponse.model_validate(wp)


@router.patch("/work-plans/{plan_id}", response_model=WorkPlanResponse)
async def patch_work_plan(
    plan_id: int,
    body: WorkPlanUpdate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    wp = await summit_service.update_work_plan(db, plan_id, body.model_dump(exclude_unset=True))
    return WorkPlanResponse.model_validate(wp)


@router.delete("/work-plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    await summit_service.delete_work_plan(db, plan_id)


@router.get("/work-plans/recent", response_model=List[dict])
async def get_recent_work_plans(
    username: str = Query(..., description="Username to filter by (requestor / assigned1)"),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    rows = await summit_service.get_recent_work_plans(db, username=username, limit=limit)
    result = []
    for r in rows:
        wp_dict = WorkPlanResponse.model_validate(r["wp"]).model_dump()
        wp_dict["log_date"] = r["log_date"]
        result.append(wp_dict)
    return result


class CopyWorkPlanBody(BaseModel):
    target_date: date


@router.post("/work-plans/{plan_id}/copy", response_model=WorkPlanResponse, status_code=status.HTTP_201_CREATED)
async def copy_work_plan(
    plan_id: int,
    body: CopyWorkPlanBody,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    username = (current_user or {}).get("username") or "system"
    wp = await summit_service.copy_work_plan(db, plan_id, body.target_date, username=username)
    return WorkPlanResponse.model_validate(wp)


class SendEmailBody(BaseModel):
    email_type: str = "to"


@router.get("/day/{log_date}/email/preview")
async def preview_day_email(
    log_date: date,
    email_type: str = Query("to", description="Email type: to | dc | smoka"),
    db: AsyncSession = Depends(get_summit_db),
):
    """Return the plain-text email body without sending it."""
    payload = await summit_service.get_daily_view(db=db, log_date=log_date)
    day_data = {
        "crew_assignments": payload.get("crew") or [],
        "weather": payload.get("weather"),
        "programs": payload.get("programs") or [],
        "work_plans": payload.get("work_plans") or [],
        "log_items": payload.get("log_items") or [],
    }
    body = summit_service._build_email_body(log_date, day_data, email_type)
    return {"email_type": email_type, "log_date": str(log_date), "body": body}


@router.post("/day/{log_date}/email/send")
async def send_day_email(
    log_date: date,
    body: SendEmailBody,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    username = (current_user or {}).get("username") or "system"
    return await summit_service.send_summit_email(db, log_date, body.email_type, username)


# ── Log Items ───────────────────────────────────────────────────────────────────
@router.post("/day/{log_date}/items", response_model=LogItemResponse, status_code=status.HTTP_201_CREATED)
async def create_log_item(
    log_date: date,
    body: LogItemCreate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    item = await summit_service.create_log_item(db, log_date, body.model_dump())
    return LogItemResponse.model_validate(item)


@router.get("/items/{item_id}", response_model=LogItemResponse)
async def get_log_item(item_id: int, db: AsyncSession = Depends(get_summit_db)):
    item = await summit_service.get_log_item(db, item_id)
    return LogItemResponse.model_validate(item)


@router.patch("/items/{item_id}", response_model=LogItemResponse)
async def patch_log_item(
    item_id: int,
    body: LogItemUpdate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    username = (current_user or {}).get("username") or "system"
    item = await summit_service.update_log_item(db, item_id, body.model_dump(exclude_unset=True), username=username)
    return LogItemResponse.model_validate(item)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_log_item(
    item_id: int,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    await summit_service.delete_log_item(db, item_id)


# ── Search ──────────────────────────────────────────────────────────────────────
@router.get("/search", response_model=LogSearchResponse)
async def search_log_items(
    q: str = Query(..., min_length=1),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    crew_tab: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_summit_db),
):
    rows, total = await summit_service.search_log_items(
        db, q=q, from_date=from_date, to_date=to_date, crew_tab=crew_tab, limit=limit, offset=offset,
    )
    items_out = []
    for r in rows:
        resp = LogItemResponse.model_validate(r["item"])
        resp.log_date = r["log_date"]
        items_out.append(resp)
    return LogSearchResponse(items=items_out, total=total)
