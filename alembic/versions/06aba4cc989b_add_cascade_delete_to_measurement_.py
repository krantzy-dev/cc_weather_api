"""add cascade delete to measurement foreign keys

Revision ID: 06aba4cc989b
Revises: d66a43b0fead
Create Date: 2026-07-12 14:42:05.711164

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "06aba4cc989b"
down_revision: str | Sequence[str] | None = "d66a43b0fead"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("fk_measurement_location_id_location", "measurement", type_="foreignkey")
    op.create_foreign_key(
        "fk_measurement_location_id_location",
        "measurement",
        "location",
        ["location_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint("fk_measurement_metric_id_metric", "measurement", type_="foreignkey")
    op.create_foreign_key(
        "fk_measurement_metric_id_metric",
        "measurement",
        "metric",
        ["metric_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_measurement_metric_id_metric", "measurement", type_="foreignkey")
    op.create_foreign_key(
        "fk_measurement_metric_id_metric", "measurement", "metric", ["metric_id"], ["id"]
    )

    op.drop_constraint("fk_measurement_location_id_location", "measurement", type_="foreignkey")
    op.create_foreign_key(
        "fk_measurement_location_id_location", "measurement", "location", ["location_id"], ["id"]
    )
