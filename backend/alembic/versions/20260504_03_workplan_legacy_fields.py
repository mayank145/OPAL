"""Add legacy WorkPlan fields: requestor, status, type, subsystem, plan_text,
warnings, teampass, realstart/end, req_flags, lockout_flags, completion_title

Revision ID: 20260504_03
Revises: 20260504_02_widen_label_melco_fai
Create Date: 2026-05-04
"""
from alembic import op
import sqlalchemy as sa

revision = "20260504_03"
down_revision = "20260504_02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("work_plans", sa.Column("requestor",        sa.String(40),  nullable=True))
    op.add_column("work_plans", sa.Column("wp_status",        sa.String(20),  nullable=True))
    op.add_column("work_plans", sa.Column("wp_type",          sa.String(20),  nullable=True))
    op.add_column("work_plans", sa.Column("wp_subsystem",     sa.String(20),  nullable=True))
    op.add_column("work_plans", sa.Column("plan_text",        sa.Text(),      nullable=True))
    op.add_column("work_plans", sa.Column("day_warning",      sa.String(200), nullable=True))
    op.add_column("work_plans", sa.Column("nite_warning",     sa.String(200), nullable=True))
    op.add_column("work_plans", sa.Column("teampass",         sa.String(80),  nullable=True))
    op.add_column("work_plans", sa.Column("realstart",        sa.DateTime(timezone=True), nullable=True))
    op.add_column("work_plans", sa.Column("realend",          sa.DateTime(timezone=True), nullable=True))
    op.add_column("work_plans", sa.Column("req_flags",        sa.Text(),      nullable=True))
    op.add_column("work_plans", sa.Column("lockout_flags",    sa.Text(),      nullable=True))
    op.add_column("work_plans", sa.Column("completion_title", sa.String(200), nullable=True))


def downgrade() -> None:
    for col in ["requestor", "wp_status", "wp_type", "wp_subsystem", "plan_text",
                "day_warning", "nite_warning", "teampass", "realstart", "realend",
                "req_flags", "lockout_flags", "completion_title"]:
        op.drop_column("work_plans", col)
