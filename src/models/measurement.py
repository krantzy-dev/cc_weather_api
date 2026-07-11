# src/models/measurement.py
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Measurement(Base):
    __tablename__ = "measurement"

    id: Mapped[int] = mapped_column(primary_key=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"), index=True)
    metric_id: Mapped[int] = mapped_column(ForeignKey("metric.id"), index=True)
    ts_value: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    ts_created: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    forecast_horizon: Mapped[int]
    value: Mapped[float]
