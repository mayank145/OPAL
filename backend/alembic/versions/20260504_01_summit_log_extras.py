"""Summit: log item summit_access, day zoom fields

Revision ID: 20260504_01
Revises: 20260331_01
Create Date: 2026-05-04
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260504_01"
down_revision: Union[str, None] = "20260331_01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("log_items", sa.Column("summit_access", sa.String(length=20), nullable=True))
    op.add_column("summit_days", sa.Column("zoom_meeting_id", sa.String(length=64), nullable=True))
    op.add_column("summit_days", sa.Column("zoom_password", sa.String(length=64), nullable=True))
    op.add_column("summit_days", sa.Column("zoom_join_url", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("summit_days", "zoom_join_url")
    op.drop_column("summit_days", "zoom_password")
    op.drop_column("summit_days", "zoom_meeting_id")
    op.drop_column("log_items", "summit_access")
