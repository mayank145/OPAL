"""create summit schema

Revision ID: 20260325_01
Revises:
Create Date: 2026-03-25 10:40:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "20260325_01"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "summit_days",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("legacy_day_id", sa.Integer(), nullable=True),
        sa.Column("log_date", sa.Date(), nullable=False),
        sa.Column("day_label", sa.String(length=10), nullable=True),
        sa.Column("history_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_summit_days_legacy_day_id", "summit_days", ["legacy_day_id"], unique=True)
    op.create_index("ix_summit_days_log_date", "summit_days", ["log_date"], unique=True)

    op.create_table(
        "crew_assignments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("summit_day_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", sa.String(length=10), nullable=False),
        sa.Column("member_name", sa.String(length=40), nullable=True),
        sa.Column("location", sa.String(length=30), nullable=True),
        sa.Column("time_in", sa.DateTime(timezone=True), nullable=True),
        sa.Column("time_out", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sort_order", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.CheckConstraint("role IN ('TO', 'IO', 'DC')", name="ck_crew_assignments_role"),
        sa.ForeignKeyConstraint(["summit_day_id"], ["summit_days.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_crew_assignments_role", "crew_assignments", ["role"], unique=False)
    op.create_index("ix_crew_assignments_summit_day_id", "crew_assignments", ["summit_day_id"], unique=False)
    op.create_index("ix_crew_assignments_day_sort", "crew_assignments", ["summit_day_id", "sort_order"], unique=False)

    op.create_table(
        "weather_snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("summit_day_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sky", sa.Text(), nullable=True),
        sa.Column("seeing", sa.Text(), nullable=True),
        sa.Column("temp_c", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("wind", sa.Text(), nullable=True),
        sa.Column("humidity_pct", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("comment_text", sa.Text(), nullable=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["summit_day_id"], ["summit_days.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("summit_day_id"),
    )
    op.create_index("ix_weather_snapshots_summit_day_id", "weather_snapshots", ["summit_day_id"], unique=True)

    op.create_table(
        "observation_programs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("legacy_prog_id", sa.Integer(), nullable=True),
        sa.Column("summit_day_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("program_code", sa.String(length=20), nullable=True),
        sa.Column("instr", sa.String(length=10), nullable=True),
        sa.Column("alloc", sa.String(length=10), nullable=True),
        sa.Column("pi", sa.String(length=50), nullable=True),
        sa.Column("ao1", sa.String(length=10), nullable=True),
        sa.Column("ao2", sa.String(length=10), nullable=True),
        sa.Column("slot_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("slot_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("gid", sa.String(length=10), nullable=True),
        sa.Column("propid", sa.String(length=20), nullable=True),
        sa.Column("obs1", sa.String(length=50), nullable=True),
        sa.Column("obs1loc", sa.String(length=10), nullable=True),
        sa.Column("obs2", sa.String(length=50), nullable=True),
        sa.Column("obs2loc", sa.String(length=10), nullable=True),
        sa.Column("obs3", sa.String(length=50), nullable=True),
        sa.Column("obs3loc", sa.String(length=10), nullable=True),
        sa.Column("obs4", sa.String(length=50), nullable=True),
        sa.Column("obs4loc", sa.String(length=10), nullable=True),
        sa.Column("ss", sa.String(length=30), nullable=True),
        sa.Column("ssloc", sa.String(length=10), nullable=True),
        sa.Column("ss2", sa.String(length=30), nullable=True),
        sa.Column("ss2loc", sa.String(length=10), nullable=True),
        sa.Column("others1", sa.String(length=50), nullable=True),
        sa.Column("others1loc", sa.String(length=10), nullable=True),
        sa.Column("others2", sa.String(length=50), nullable=True),
        sa.Column("others2loc", sa.String(length=10), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("comment_text", sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(["summit_day_id"], ["summit_days.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_observation_programs_legacy_prog_id", "observation_programs", ["legacy_prog_id"], unique=True)
    op.create_index("ix_observation_programs_summit_day_id", "observation_programs", ["summit_day_id"], unique=False)
    op.create_index(
        "ix_observation_programs_day_sort",
        "observation_programs",
        ["summit_day_id", "sort_order"],
        unique=False,
    )

    op.create_table(
        "work_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("summit_day_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("copied_from_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("window_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("window_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("nite_effect", sa.String(length=100), nullable=True),
        sa.Column("day_effect", sa.String(length=100), nullable=True),
        sa.Column("location", sa.String(length=20), nullable=True),
        sa.Column("location2", sa.String(length=20), nullable=True),
        sa.Column("location3", sa.String(length=20), nullable=True),
        sa.Column("assigned1", sa.String(length=30), nullable=True),
        sa.Column("assigned2", sa.String(length=50), nullable=True),
        sa.Column("dcassist", sa.String(length=10), nullable=True),
        sa.Column("notify", sa.String(length=20), nullable=True),
        sa.Column("contact1", sa.String(length=20), nullable=True),
        sa.Column("contact2", sa.String(length=50), nullable=True),
        sa.Column("others", sa.String(length=50), nullable=True),
        sa.Column("otherreq", sa.String(length=40), nullable=True),
        sa.Column("comptitle", sa.String(length=200), nullable=True),
        sa.Column("comptext", sa.Text(), nullable=True),
        sa.Column("master", sa.Integer(), nullable=True),
        sa.Column("intervene", sa.String(length=20), nullable=True),
        sa.Column("melco", sa.String(length=3), nullable=True),
        sa.Column("fai", sa.String(length=3), nullable=True),
        sa.Column("seats", sa.Integer(), nullable=True),
        sa.Column("seats2", sa.Integer(), nullable=True),
        sa.Column("pseats", sa.Integer(), nullable=True),
        sa.Column("pass_text", sa.String(length=80), nullable=True),
        sa.Column("rpass_text", sa.String(length=80), nullable=True),
        sa.Column("requirements", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["copied_from_id"], ["work_plans.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["summit_day_id"], ["summit_days.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_work_plans_summit_day_id", "work_plans", ["summit_day_id"], unique=False)

    op.create_table(
        "log_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("legacy_item_id", sa.Integer(), nullable=True),
        sa.Column("legacy_old_item_id", sa.Integer(), nullable=True),
        sa.Column("summit_day_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("work_plan_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("crew_tab", sa.String(length=10), server_default=sa.text("'ALL'"), nullable=False),
        sa.Column("item_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=True),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("item_type", sa.String(length=16), nullable=True),
        sa.Column("downtime_minutes", sa.Integer(), nullable=True),
        sa.Column("subsystem", sa.String(length=10), nullable=True),
        sa.Column("status", sa.String(length=15), nullable=True),
        sa.Column("created_by", sa.String(length=20), nullable=True),
        sa.Column("history_text", sa.Text(), nullable=True),
        sa.Column("comment_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("crew_tab IN ('ALL', 'TO', 'IO', 'DC', 'WP', 'TO-IO')", name="ck_log_items_crew_tab"),
        sa.ForeignKeyConstraint(["summit_day_id"], ["summit_days.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["work_plan_id"], ["work_plans.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_log_items_legacy_item_id", "log_items", ["legacy_item_id"], unique=True)
    op.create_index("ix_log_items_legacy_old_item_id", "log_items", ["legacy_old_item_id"], unique=False)
    op.create_index("ix_log_items_summit_day_id", "log_items", ["summit_day_id"], unique=False)
    op.create_index("ix_log_items_work_plan_id", "log_items", ["work_plan_id"], unique=False)
    op.create_index("ix_log_items_day_crew", "log_items", ["summit_day_id", "crew_tab"], unique=False)
    op.execute(
        "CREATE INDEX ix_log_items_search ON log_items USING gin "
        "(to_tsvector('english', coalesce(title, '') || ' ' || coalesce(body, '')))"
    )

    op.create_table(
        "work_plan_item_links",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("work_plan_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("linked_legacy_item_id", sa.Integer(), nullable=False),
        sa.Column("link_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["work_plan_id"], ["work_plans.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("work_plan_id", "link_order", name="uq_work_plan_item_links_order"),
    )
    op.create_index("ix_work_plan_item_links_work_plan_id", "work_plan_item_links", ["work_plan_id"], unique=False)
    op.create_index(
        "ix_work_plan_item_links_linked_legacy_item_id",
        "work_plan_item_links",
        ["linked_legacy_item_id"],
        unique=False,
    )

    op.create_table(
        "email_deliveries",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("summit_day_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("mailed", sa.String(length=1), nullable=True),
        sa.Column("mailtime", sa.DateTime(timezone=True), nullable=True),
        sa.Column("mailsmoka", sa.String(length=1), nullable=True),
        sa.Column("smokatime", sa.DateTime(timezone=True), nullable=True),
        sa.Column("mailday", sa.String(length=1), nullable=True),
        sa.Column("maildtime", sa.DateTime(timezone=True), nullable=True),
        sa.Column("am_sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("pm_sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("day_digest_sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["summit_day_id"], ["summit_days.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("summit_day_id"),
    )
    op.create_index("ix_email_deliveries_summit_day_id", "email_deliveries", ["summit_day_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_email_deliveries_summit_day_id", table_name="email_deliveries")
    op.drop_table("email_deliveries")

    op.drop_index("ix_work_plan_item_links_linked_legacy_item_id", table_name="work_plan_item_links")
    op.drop_index("ix_work_plan_item_links_work_plan_id", table_name="work_plan_item_links")
    op.drop_table("work_plan_item_links")

    op.drop_index("ix_log_items_day_crew", table_name="log_items")
    op.drop_index("ix_log_items_work_plan_id", table_name="log_items")
    op.drop_index("ix_log_items_summit_day_id", table_name="log_items")
    op.drop_index("ix_log_items_legacy_old_item_id", table_name="log_items")
    op.drop_index("ix_log_items_legacy_item_id", table_name="log_items")
    op.execute("DROP INDEX IF EXISTS ix_log_items_search")
    op.drop_table("log_items")

    op.drop_index("ix_work_plans_summit_day_id", table_name="work_plans")
    op.drop_table("work_plans")

    op.drop_index("ix_observation_programs_day_sort", table_name="observation_programs")
    op.drop_index("ix_observation_programs_summit_day_id", table_name="observation_programs")
    op.drop_index("ix_observation_programs_legacy_prog_id", table_name="observation_programs")
    op.drop_table("observation_programs")

    op.drop_index("ix_weather_snapshots_summit_day_id", table_name="weather_snapshots")
    op.drop_table("weather_snapshots")

    op.drop_index("ix_crew_assignments_day_sort", table_name="crew_assignments")
    op.drop_index("ix_crew_assignments_summit_day_id", table_name="crew_assignments")
    op.drop_index("ix_crew_assignments_role", table_name="crew_assignments")
    op.drop_table("crew_assignments")

    op.drop_index("ix_summit_days_log_date", table_name="summit_days")
    op.drop_index("ix_summit_days_legacy_day_id", table_name="summit_days")
    op.drop_table("summit_days")
