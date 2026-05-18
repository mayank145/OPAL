"""
Summit Logging API — full CRUD for all entities.
"""
from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from fastapi import APIRouter, Body, Depends, Query, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import require_auth
from app.db.session import get_summit_db
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


# ── Health ──────────────────────────────────────────────────────────────────────
@router.get("/health")
async def summit_health(db: AsyncSession = Depends(get_summit_db)):
    result = await db.execute(text("SELECT 1"))
    result.scalar_one()
    return {"status": "healthy", "database": "postgres", "service": "summit-logging"}


# ── Monthly ─────────────────────────────────────────────────────────────────────
@router.get("/monthly", response_model=dict)
async def monthly(
    year: int = Query(..., ge=1900, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: AsyncSession = Depends(get_summit_db),
):
    """Monthly calendar: returns day headers with entry count and downtime totals."""
    entries = await summit_service.get_monthly_days(db=db, year=year, month=month)
    days_out = []
    for e in entries:
        d = e["day"]
        days_out.append(
            SummitMonthlyDayResponse(
                id=d.id,
                log_date=d.log_date,
                day_label=d.day_label,
                history_text=d.history_text,
                entry_count=e["entry_count"],
                total_downtime=e["total_downtime"],
                first_instr=None,
            )
        )
    return {"year": year, "month": month, "days": days_out}


@router.get("/year/{year}", response_model=dict)
async def yearly(
    year: int,
    db: AsyncSession = Depends(get_summit_db),
):
    """Year overview (legacy loglist): each day with counts, downtime, first program instrument."""
    entries = await summit_service.get_yearly_days(db=db, year=year)
    days_out = []
    for e in entries:
        d = e["day"]
        days_out.append(
            SummitMonthlyDayResponse(
                id=d.id,
                log_date=d.log_date,
                day_label=d.day_label,
                history_text=d.history_text,
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
    """Create a new summit day (for dates that don't yet have a log record)."""
    day = await summit_service.create_summit_day(
        db, body.log_date, body.day_label, body.history_text
    )
    return SummitMonthlyDayResponse(
        id=day.id, log_date=day.log_date, day_label=day.day_label,
        history_text=day.history_text,
    )


@router.get("/day/{log_date}", response_model=SummitDailyViewResponse)
async def day_view(log_date: date, db: AsyncSession = Depends(get_summit_db)):
    """Full daily view: crew + weather + programs + work plans + log items."""
    payload = await summit_service.get_daily_view(db=db, log_date=log_date)
    day = payload["day"]
    return SummitDailyViewResponse(
        id=day.id,
        log_date=day.log_date,
        day_label=day.day_label,
        history_text=day.history_text,
        zoom_meeting_id=day.zoom_meeting_id,
        zoom_password=day.zoom_password,
        zoom_join_url=day.zoom_join_url,
        entry_count=payload["entry_count"],
        total_downtime=payload["total_downtime"],
        crew_assignments=[CrewAssignmentResponse.model_validate(c) for c in payload["crew"]],
        weather=WeatherSnapshotResponse.model_validate(payload["weather"]) if payload["weather"] else None,
        programs=[ObservationProgramResponse.model_validate(p) for p in payload["programs"]],
        work_plans=[WorkPlanResponse.model_validate(wp) for wp in payload["work_plans"]],
        log_items=[LogItemResponse.model_validate(li) for li in payload["log_items"]],
        email_delivery=EmailDeliveryResponse.model_validate(payload["email_delivery"]) if payload["email_delivery"] else None,
    )


@router.patch("/day/{log_date}", response_model=SummitMonthlyDayResponse)
async def patch_summit_day(
    log_date: date,
    body: SummitDayUpdate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    """Update summit day header fields (day_label, history_text)."""
    data = body.model_dump(exclude_unset=True)
    day = await summit_service.update_summit_day(db, log_date, data)
    return SummitMonthlyDayResponse(
        id=day.id, log_date=day.log_date, day_label=day.day_label,
        history_text=day.history_text,
        zoom_meeting_id=day.zoom_meeting_id,
        zoom_password=day.zoom_password,
        zoom_join_url=day.zoom_join_url,
    )


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
    crew_id: UUID,
    body: CrewAssignmentUpdate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    row = await summit_service.update_crew(db, crew_id, body.model_dump(exclude_unset=True))
    return CrewAssignmentResponse.model_validate(row)


@router.delete("/crew/{crew_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_crew(crew_id: UUID, db: AsyncSession = Depends(get_summit_db), current_user: dict = Depends(require_auth)):
    await summit_service.delete_crew(db, crew_id)


# ── Weather Snapshots ───────────────────────────────────────────────────────────
@router.put("/day/{log_date}/weather", response_model=WeatherSnapshotResponse)
async def upsert_weather(
    log_date: date,
    body: WeatherSnapshotUpdate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    """Create or update weather snapshot for a day."""
    snap = await summit_service.upsert_weather(db, log_date, body.model_dump(exclude_unset=True))
    return WeatherSnapshotResponse.model_validate(snap)


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
    program_id: UUID,
    body: ObservationProgramUpdate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    p = await summit_service.update_program(db, program_id, body.model_dump(exclude_unset=True))
    return ObservationProgramResponse.model_validate(p)


@router.delete("/programs/{program_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_program(program_id: UUID, db: AsyncSession = Depends(get_summit_db), current_user: dict = Depends(require_auth)):
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
    plan_id: UUID,
    body: WorkPlanUpdate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    wp = await summit_service.update_work_plan(db, plan_id, body.model_dump(exclude_unset=True))
    return WorkPlanResponse.model_validate(wp)


@router.delete("/work-plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_plan(plan_id: UUID, db: AsyncSession = Depends(get_summit_db), current_user: dict = Depends(require_auth)):
    await summit_service.delete_work_plan(db, plan_id)


@router.get("/work-plans/recent", response_model=List[dict])
async def get_recent_work_plans(
    username: str = Query(..., description="Username to filter by (requestor / assigned1)"),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    """Return the last N work plans associated with a user (for Copy from Previous)."""
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
    plan_id: UUID,
    body: CopyWorkPlanBody,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    """Duplicate a work plan onto a different log date."""
    username = (current_user or {}).get("username") or "system"
    wp = await summit_service.copy_work_plan(db, plan_id, body.target_date, username=username)
    return WorkPlanResponse.model_validate(wp)


class SendEmailBody(BaseModel):
    email_type: str = "to"   # "to" | "dc" | "smoka"


@router.post("/day/{log_date}/email/send")
async def send_day_email(
    log_date: date,
    body: SendEmailBody,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    """Compose and send a night-log / DC / SMOKA email for the given day."""
    username = (current_user or {}).get("username") or "system"
    result = await summit_service.send_summit_email(db, log_date, body.email_type, username)
    return result


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
async def get_log_item(item_id: UUID, db: AsyncSession = Depends(get_summit_db)):
    item = await summit_service.get_log_item(db, item_id)
    return LogItemResponse.model_validate(item)


@router.patch("/items/{item_id}", response_model=LogItemResponse)
async def patch_log_item(
    item_id: UUID,
    body: LogItemUpdate,
    db: AsyncSession = Depends(get_summit_db),
    current_user: dict = Depends(require_auth),
):
    username = (current_user or {}).get("username") or "system"
    item = await summit_service.update_log_item(db, item_id, body.model_dump(exclude_unset=True), username=username)
    return LogItemResponse.model_validate(item)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_log_item(item_id: UUID, db: AsyncSession = Depends(get_summit_db), current_user: dict = Depends(require_auth)):
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
    """Search log items (case-insensitive substring). Results include log_date."""
    rows, total = await summit_service.search_log_items(
        db, q=q, from_date=from_date, to_date=to_date, crew_tab=crew_tab, limit=limit, offset=offset,
    )
    items_out = []
    for r in rows:
        resp = LogItemResponse.model_validate(r["item"])
        resp.log_date = r["log_date"]
        items_out.append(resp)
    return LogSearchResponse(items=items_out, total=total)
