# src/models/measurement.py
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Measurement(Base):
    __tablename__ = "measurement"
    __table_args__ = (UniqueConstraint("location_id", "metric_id", "ts_value", "forecast_horizon"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    location_id: Mapped[int] = mapped_column(
        ForeignKey("location.id", ondelete="CASCADE"), index=True
    )
    metric_id: Mapped[int] = mapped_column(ForeignKey("metric.id", ondelete="CASCADE"), index=True)
    ts_value: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    ts_created: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    forecast_horizon: Mapped[int]
    value: Mapped[float]
