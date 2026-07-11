from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
