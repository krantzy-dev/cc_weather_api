from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import Metric


def list_all(db: Session) -> list[Metric]:
    """Retrieve all metrics.

    Args:
        db: Database session.

    Returns:
        Every metric currently stored.
    """
    return db.execute(select(Metric)).scalars().all()


def create(db: Session, name: str, unit: str) -> Metric:
    """Insert a new location.

    Args:
        db: Database session.
        name: Human-readable label for the location.
        lat: Latitude in decimal degrees.
        lon: Longitude in decimal degrees.

    Returns:
        The newly created, persisted location.
    """
    metric = Metric(name=name, unit=unit)
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric
