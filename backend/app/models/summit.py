"""
Summit Logging models backed by Postgres.
"""
import enum
import uuid

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import SummitBase


class CrewRole(str, enum.Enum):
    TO = "TO"
    IO = "IO"
    DC = "DC"


class LogCrewTab(str, enum.Enum):
    ALL = "ALL"
    TO = "TO"
    IO = "IO"
    DC = "DC"
    WP = "WP"
    TO_IO = "TO-IO"


class SummitDay(SummitBase):
    __tablename__ = "summit_days"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    legacy_day_id = Column(Integer, unique=True, index=True)
    log_date = Column(Date, nullable=False, unique=True, index=True)
    day_label = Column(String(80))
    history_text = Column(Text)
    zoom_meeting_id = Column(String(64))
    zoom_password = Column(String(64))
    zoom_join_url = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=text("now()"), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=text("now()"),
        onupdate=text("now()"),
        nullable=False,
    )


class CrewAssignment(SummitBase):
    __tablename__ = "crew_assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    summit_day_id = Column(UUID(as_uuid=True), ForeignKey("summit_days.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(10), nullable=False, index=True)
    member_name = Column(String(40))
    location = Column(String(30))
    time_in = Column(DateTime(timezone=True))
    time_out = Column(DateTime(timezone=True))
    sort_order = Column(Integer, nullable=False, server_default=text("0"))

    __table_args__ = (
        CheckConstraint("role IN ('TO', 'IO', 'DC')", name="ck_crew_assignments_role"),
        Index("ix_crew_assignments_day_sort", "summit_day_id", "sort_order"),
    )


class WeatherSnapshot(SummitBase):
    __tablename__ = "weather_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    summit_day_id = Column(
        UUID(as_uuid=True),
        ForeignKey("summit_days.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    sky = Column(Text)
    seeing = Column(Text)
    temp_raw = Column(Text)
    temp_c = Column(Numeric(5, 2))
    wind = Column(Text)
    humidity_raw = Column(Text)
    humidity_pct = Column(Numeric(5, 2))
    comment_text = Column(Text)
    captured_at = Column(DateTime(timezone=True))


class ObservationProgram(SummitBase):
    __tablename__ = "observation_programs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    legacy_prog_id = Column(Integer, unique=True, index=True)
    summit_day_id = Column(UUID(as_uuid=True), ForeignKey("summit_days.id", ondelete="CASCADE"), nullable=False, index=True)
    sort_order = Column(Integer, nullable=False, server_default=text("0"))

    program_code = Column(String(20))
    instr = Column(String(10))
    alloc = Column(String(10))
    pi = Column(String(50))
    ao1 = Column(String(10))
    ao2 = Column(String(10))
    slot_start = Column(DateTime(timezone=True))
    slot_end = Column(DateTime(timezone=True))
    gid = Column(String(10))
    propid = Column(String(20))

    obs1 = Column(String(50))
    obs1loc = Column(String(10))
    obs2 = Column(String(50))
    obs2loc = Column(String(10))
    obs3 = Column(String(50))
    obs3loc = Column(String(10))
    obs4 = Column(String(50))
    obs4loc = Column(String(10))

    ss = Column(String(30))
    ssloc = Column(String(10))
    ss2 = Column(String(30))
    ss2loc = Column(String(10))

    others1 = Column(String(50))
    others1loc = Column(String(10))
    others2 = Column(String(50))
    others2loc = Column(String(10))
    notes = Column(Text)
    comment_text = Column(String(100))

    __table_args__ = (
        Index("ix_observation_programs_day_sort", "summit_day_id", "sort_order"),
    )


class WorkPlan(SummitBase):
    __tablename__ = "work_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    summit_day_id = Column(UUID(as_uuid=True), ForeignKey("summit_days.id", ondelete="CASCADE"), nullable=False, index=True)
    copied_from_id = Column(UUID(as_uuid=True), ForeignKey("work_plans.id", ondelete="SET NULL"))

    window_start = Column(DateTime(timezone=True))
    window_end = Column(DateTime(timezone=True))

    # Plan header
    requestor = Column(String(40))
    wp_status = Column(String(20))          # Planned / InProgress / Completed / Cancelled
    wp_type = Column(String(20))
    wp_subsystem = Column(String(20))
    plan_text = Column(Text)               # description of the work
    day_warning = Column(String(200))
    nite_warning = Column(String(200))
    teampass = Column(String(80))
    realstart = Column(DateTime(timezone=True))
    realend = Column(DateTime(timezone=True))

    # Required / LockOut flags (comma-separated keys)
    req_flags = Column(Text)              # e.g. "Move-Tel,Move-EL,80t-Crane"
    lockout_flags = Column(Text)          # e.g. "No-Tel-Move,No-AZ-Move"

    nite_effect = Column(String(100))
    day_effect = Column(String(100))
    location = Column(String(20))
    location2 = Column(String(20))
    location3 = Column(String(20))
    assigned1 = Column(String(30))
    assigned2 = Column(String(50))
    dcassist = Column(String(10))
    notify = Column(String(20))
    contact1 = Column(String(20))
    contact2 = Column(String(50))
    others = Column(String(50))
    otherreq = Column(String(40))
    comptitle = Column(String(200))        # plan title (legacy: Plan Title)
    comptext = Column(Text)                # completion text
    completion_title = Column(String(200)) # filled after completion
    master = Column(Integer)
    intervene = Column(String(20))
    melco = Column(String(20))
    fai = Column(String(20))
    seats = Column(Integer)
    seats2 = Column(Integer)
    pseats = Column(Integer)
    pass_text = Column(String(80))
    rpass_text = Column(String(80))
    requirements = Column(Text)
    notes = Column(Text)


class LogItem(SummitBase):
    __tablename__ = "log_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    legacy_item_id = Column(Integer, unique=True, index=True)
    legacy_old_item_id = Column(Integer, index=True)
    summit_day_id = Column(UUID(as_uuid=True), ForeignKey("summit_days.id", ondelete="CASCADE"), nullable=False, index=True)
    work_plan_id = Column(UUID(as_uuid=True), ForeignKey("work_plans.id", ondelete="SET NULL"), index=True)

    crew_tab = Column(String(10), nullable=False, server_default=text("'ALL'"))
    item_time = Column(DateTime(timezone=True))
    title = Column(String(200))
    body = Column(Text)
    item_type = Column(String(16))
    downtime_minutes = Column(Integer)
    subsystem = Column(String(10))
    status = Column(String(15))
    created_by = Column(String(20))
    history_text = Column(Text)
    comment_text = Column(Text)
    summit_access = Column(String(20))
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint("crew_tab IN ('ALL', 'TO', 'IO', 'DC', 'WP', 'TO-IO')", name="ck_log_items_crew_tab"),
        Index("ix_log_items_day_crew", "summit_day_id", "crew_tab"),
        Index(
            "ix_log_items_search",
            text("to_tsvector('english', coalesce(title, '') || ' ' || coalesce(body, ''))"),
            postgresql_using="gin",
        ),
    )


class WorkPlanItemLink(SummitBase):
    __tablename__ = "work_plan_item_links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_plan_id = Column(UUID(as_uuid=True), ForeignKey("work_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    linked_legacy_item_id = Column(Integer, nullable=False, index=True)
    link_order = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("work_plan_id", "link_order", name="uq_work_plan_item_links_order"),
    )


class EmailDelivery(SummitBase):
    __tablename__ = "email_deliveries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    summit_day_id = Column(
        UUID(as_uuid=True),
        ForeignKey("summit_days.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    mailed = Column(String(1))
    mailtime = Column(DateTime(timezone=True))
    mailsmoka = Column(String(1))
    smokatime = Column(DateTime(timezone=True))
    mailday = Column(String(1))
    maildtime = Column(DateTime(timezone=True))
    am_sent_at = Column(DateTime(timezone=True))
    pm_sent_at = Column(DateTime(timezone=True))
    day_digest_sent_at = Column(DateTime(timezone=True))
    last_error = Column(Text)
