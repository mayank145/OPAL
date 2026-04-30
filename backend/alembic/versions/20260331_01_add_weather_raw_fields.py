"""add raw weather text fields

Revision ID: 20260331_01
Revises: 20260325_01
Create Date: 2026-03-31 01:40:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260331_01"
down_revision: Union[str, None] = "20260325_01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("weather_snapshots", sa.Column("temp_raw", sa.Text(), nullable=True))
    op.add_column("weather_snapshots", sa.Column("humidity_raw", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("weather_snapshots", "humidity_raw")
    op.drop_column("weather_snapshots", "temp_raw")

