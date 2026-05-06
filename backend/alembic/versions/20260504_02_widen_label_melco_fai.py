"""Widen day_label to 80, melco/fai to 20

Revision ID: 20260504_02
Revises: 20260504_01
Create Date: 2026-05-04
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260504_02"
down_revision: Union[str, None] = "20260504_01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("summit_days", "day_label",
                    existing_type=sa.String(10),
                    type_=sa.String(80),
                    existing_nullable=True)
    op.alter_column("work_plans", "melco",
                    existing_type=sa.String(3),
                    type_=sa.String(20),
                    existing_nullable=True)
    op.alter_column("work_plans", "fai",
                    existing_type=sa.String(3),
                    type_=sa.String(20),
                    existing_nullable=True)


def downgrade() -> None:
    op.alter_column("work_plans", "fai",
                    existing_type=sa.String(20),
                    type_=sa.String(3),
                    existing_nullable=True)
    op.alter_column("work_plans", "melco",
                    existing_type=sa.String(20),
                    type_=sa.String(3),
                    existing_nullable=True)
    op.alter_column("summit_days", "day_label",
                    existing_type=sa.String(80),
                    type_=sa.String(10),
                    existing_nullable=True)
