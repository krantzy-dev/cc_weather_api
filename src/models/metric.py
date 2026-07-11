# src/models/metric.py
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Metric(Base):
    __tablename__ = "metric"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    unit: Mapped[str | None]
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
