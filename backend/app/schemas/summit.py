"""
Pydantic schemas for Summit Logging API — full CRUD coverage.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

# ── Shared validator ────────────────────────────────────────────────────────────
_CREW_TAB = ("ALL", "TO", "IO", "DC", "WP", "TO-IO")
_CREW_ROLE = ("TO", "IO", "DC")


def _validate_crew_tab(v: str) -> str:
    u = v.strip().upper() if isinstance(v, str) else v
    if u not in _CREW_TAB:
        raise ValueError(f"crew_tab must be one of {_CREW_TAB}")
    return u


def _validate_crew_role(v: str) -> str:
    u = v.strip().upper() if isinstance(v, str) else v
    if u not in _CREW_ROLE:
        raise ValueError(f"role must be one of {_CREW_ROLE}")
    return u


# ── Summit Day ──────────────────────────────────────────────────────────────────
class SummitDayCreate(BaseModel):
    log_date: date
    day_label: Optional[str] = Field(None, max_length=10)
    history_text: Optional[str] = None


class SummitDayUpdate(BaseModel):
    day_label: Optional[str] = Field(None, max_length=10)
    history_text: Optional[str] = None


class SummitMonthlyDayResponse(BaseModel):
    id: UUID
    log_date: date
    day_label: Optional[str] = None
    history_text: Optional[str] = None
    entry_count: int = 0
    total_downtime: int = 0

    class Config:
        from_attributes = True


# ── Crew Assignments ────────────────────────────────────────────────────────────
class CrewAssignmentCreate(BaseModel):
    role: str
    member_name: Optional[str] = Field(None, max_length=40)
    location: Optional[str] = Field(None, max_length=30)
    time_in: Optional[datetime] = None
    time_out: Optional[datetime] = None
    sort_order: Optional[int] = None

    @field_validator("role")
    @classmethod
    def role_ok(cls, v: str) -> str:
        return _validate_crew_role(v)


class CrewAssignmentUpdate(BaseModel):
    role: Optional[str] = None
    member_name: Optional[str] = Field(None, max_length=40)
    location: Optional[str] = Field(None, max_length=30)
    time_in: Optional[datetime] = None
    time_out: Optional[datetime] = None
    sort_order: Optional[int] = None

    @field_validator("role")
    @classmethod
    def role_ok(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        return _validate_crew_role(v)


class CrewAssignmentResponse(BaseModel):
    id: UUID
    summit_day_id: UUID
    role: str
    member_name: Optional[str] = None
    location: Optional[str] = None
    time_in: Optional[datetime] = None
    time_out: Optional[datetime] = None
    sort_order: int

    class Config:
        from_attributes = True


# ── Weather Snapshots ───────────────────────────────────────────────────────────
class WeatherSnapshotUpdate(BaseModel):
    sky: Optional[str] = None
    seeing: Optional[str] = None
    temp_raw: Optional[str] = None
    wind: Optional[str] = None
    humidity_raw: Optional[str] = None
    comment_text: Optional[str] = None
    captured_at: Optional[datetime] = None


class WeatherSnapshotResponse(BaseModel):
    id: UUID
    sky: Optional[str] = None
    seeing: Optional[str] = None
    temp_raw: Optional[str] = None
    temp_c: Optional[float] = None
    wind: Optional[str] = None
    humidity_raw: Optional[str] = None
    humidity_pct: Optional[float] = None
    comment_text: Optional[str] = None
    captured_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Observation Programs ────────────────────────────────────────────────────────
class ObservationProgramCreate(BaseModel):
    sort_order: Optional[int] = None
    instr: Optional[str] = Field(None, max_length=10)
    alloc: Optional[str] = Field(None, max_length=10)
    pi: Optional[str] = Field(None, max_length=50)
    ao1: Optional[str] = Field(None, max_length=10)
    ao2: Optional[str] = Field(None, max_length=10)
    slot_start: Optional[datetime] = None
    slot_end: Optional[datetime] = None
    gid: Optional[str] = Field(None, max_length=10)
    propid: Optional[str] = Field(None, max_length=20)
    obs1: Optional[str] = Field(None, max_length=50)
    obs1loc: Optional[str] = Field(None, max_length=10)
    obs2: Optional[str] = Field(None, max_length=50)
    obs2loc: Optional[str] = Field(None, max_length=10)
    obs3: Optional[str] = Field(None, max_length=50)
    obs3loc: Optional[str] = Field(None, max_length=10)
    obs4: Optional[str] = Field(None, max_length=50)
    obs4loc: Optional[str] = Field(None, max_length=10)
    ss: Optional[str] = Field(None, max_length=30)
    ssloc: Optional[str] = Field(None, max_length=10)
    ss2: Optional[str] = Field(None, max_length=30)
    ss2loc: Optional[str] = Field(None, max_length=10)
    others1: Optional[str] = Field(None, max_length=50)
    others1loc: Optional[str] = Field(None, max_length=10)
    others2: Optional[str] = Field(None, max_length=50)
    others2loc: Optional[str] = Field(None, max_length=10)
    notes: Optional[str] = None
    comment_text: Optional[str] = Field(None, max_length=100)


class ObservationProgramUpdate(ObservationProgramCreate):
    pass


class ObservationProgramResponse(BaseModel):
    id: UUID
    legacy_prog_id: Optional[int] = None
    sort_order: int
    program_code: Optional[str] = None
    instr: Optional[str] = None
    alloc: Optional[str] = None
    pi: Optional[str] = None
    ao1: Optional[str] = None
    ao2: Optional[str] = None
    slot_start: Optional[datetime] = None
    slot_end: Optional[datetime] = None
    gid: Optional[str] = None
    propid: Optional[str] = None
    obs1: Optional[str] = None
    obs1loc: Optional[str] = None
    obs2: Optional[str] = None
    obs2loc: Optional[str] = None
    obs3: Optional[str] = None
    obs3loc: Optional[str] = None
    obs4: Optional[str] = None
    obs4loc: Optional[str] = None
    ss: Optional[str] = None
    ssloc: Optional[str] = None
    ss2: Optional[str] = None
    ss2loc: Optional[str] = None
    others1: Optional[str] = None
    others1loc: Optional[str] = None
    others2: Optional[str] = None
    others2loc: Optional[str] = None
    notes: Optional[str] = None
    comment_text: Optional[str] = None

    class Config:
        from_attributes = True


# ── Work Plans ──────────────────────────────────────────────────────────────────
class WorkPlanCreate(BaseModel):
    window_start: Optional[datetime] = None
    window_end: Optional[datetime] = None
    nite_effect: Optional[str] = Field(None, max_length=100)
    day_effect: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=20)
    location2: Optional[str] = Field(None, max_length=20)
    location3: Optional[str] = Field(None, max_length=20)
    assigned1: Optional[str] = Field(None, max_length=30)
    assigned2: Optional[str] = Field(None, max_length=50)
    dcassist: Optional[str] = Field(None, max_length=10)
    notify: Optional[str] = Field(None, max_length=20)
    contact1: Optional[str] = Field(None, max_length=20)
    contact2: Optional[str] = Field(None, max_length=50)
    others: Optional[str] = Field(None, max_length=50)
    otherreq: Optional[str] = Field(None, max_length=40)
    comptitle: Optional[str] = Field(None, max_length=200)
    comptext: Optional[str] = None
    requirements: Optional[str] = None
    notes: Optional[str] = None


class WorkPlanUpdate(WorkPlanCreate):
    pass


class WorkPlanResponse(BaseModel):
    id: UUID
    summit_day_id: UUID
    window_start: Optional[datetime] = None
    window_end: Optional[datetime] = None
    nite_effect: Optional[str] = None
    day_effect: Optional[str] = None
    location: Optional[str] = None
    location2: Optional[str] = None
    location3: Optional[str] = None
    assigned1: Optional[str] = None
    assigned2: Optional[str] = None
    dcassist: Optional[str] = None
    notify: Optional[str] = None
    contact1: Optional[str] = None
    contact2: Optional[str] = None
    others: Optional[str] = None
    otherreq: Optional[str] = None
    comptitle: Optional[str] = None
    comptext: Optional[str] = None
    requirements: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


# ── Log Items ───────────────────────────────────────────────────────────────────
class LogItemCreate(BaseModel):
    crew_tab: str = "ALL"
    item_time: Optional[datetime] = None
    title: Optional[str] = None
    body: Optional[str] = None
    item_type: Optional[str] = Field(None, max_length=16)
    downtime_minutes: Optional[int] = None
    subsystem: Optional[str] = Field(None, max_length=10)
    status: Optional[str] = Field(None, max_length=15)
    created_by: Optional[str] = Field(None, max_length=20)
    history_text: Optional[str] = None
    comment_text: Optional[str] = None
    work_plan_id: Optional[UUID] = None

    @field_validator("crew_tab")
    @classmethod
    def crew_tab_ok(cls, v: str) -> str:
        return _validate_crew_tab(v)


class LogItemUpdate(BaseModel):
    crew_tab: Optional[str] = None
    item_time: Optional[datetime] = None
    title: Optional[str] = None
    body: Optional[str] = None
    item_type: Optional[str] = Field(None, max_length=16)
    downtime_minutes: Optional[int] = None
    subsystem: Optional[str] = Field(None, max_length=10)
    status: Optional[str] = Field(None, max_length=15)
    created_by: Optional[str] = Field(None, max_length=20)
    history_text: Optional[str] = None
    comment_text: Optional[str] = None
    work_plan_id: Optional[UUID] = None

    @field_validator("crew_tab")
    @classmethod
    def crew_tab_ok(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        return _validate_crew_tab(v)


class LogItemResponse(BaseModel):
    id: UUID
    summit_day_id: UUID
    work_plan_id: Optional[UUID] = None
    legacy_item_id: Optional[int] = None
    legacy_old_item_id: Optional[int] = None
    crew_tab: str
    item_time: Optional[datetime] = None
    item_type: Optional[str] = None
    subsystem: Optional[str] = None
    status: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    downtime_minutes: Optional[int] = None
    created_by: Optional[str] = None
    history_text: Optional[str] = None
    comment_text: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    log_date: Optional[date] = None  # populated in search results

    class Config:
        from_attributes = True


# ── Email Delivery ──────────────────────────────────────────────────────────────
class EmailDeliveryResponse(BaseModel):
    id: UUID
    mailed: Optional[str] = None
    mailtime: Optional[datetime] = None
    mailsmoka: Optional[str] = None
    smokatime: Optional[datetime] = None
    mailday: Optional[str] = None
    maildtime: Optional[datetime] = None
    am_sent_at: Optional[datetime] = None
    pm_sent_at: Optional[datetime] = None
    day_digest_sent_at: Optional[datetime] = None
    last_error: Optional[str] = None

    class Config:
        from_attributes = True


# ── Composite / Response wrappers ───────────────────────────────────────────────
class SummitDailyViewResponse(BaseModel):
    id: UUID
    log_date: date
    day_label: Optional[str] = None
    history_text: Optional[str] = None
    entry_count: int = 0
    total_downtime: int = 0

    crew_assignments: List[CrewAssignmentResponse] = Field(default_factory=list)
    weather: Optional[WeatherSnapshotResponse] = None
    programs: List[ObservationProgramResponse] = Field(default_factory=list)
    work_plans: List[WorkPlanResponse] = Field(default_factory=list)
    log_items: List[LogItemResponse] = Field(default_factory=list)
    email_delivery: Optional[EmailDeliveryResponse] = None


class LogSearchResponse(BaseModel):
    items: List[LogItemResponse]
    total: int
