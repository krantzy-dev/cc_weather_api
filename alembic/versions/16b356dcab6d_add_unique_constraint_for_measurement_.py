"""add unique constraint for measurement upserts

Revision ID: 16b356dcab6d
Revises: 06aba4cc989b
Create Date: 2026-07-12 19:06:04.297982

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "16b356dcab6d"
down_revision: str | Sequence[str] | None = "06aba4cc989b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "uq_measurement_location_id_metric_id_ts_value_forecast_horizon",
        "measurement",
        ["location_id", "metric_id", "ts_value", "forecast_horizon"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_measurement_location_id_metric_id_ts_value_forecast_horizon",
        "measurement",
        type_="unique",
    )
