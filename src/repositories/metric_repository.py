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
    """Insert a new metric.

    Args:
        db: Database session.
        name: Human-readable label for the metric.
        lat: Latitude in decimal degrees.
        lon: Longitude in decimal degrees.

    Returns:
        The newly created, persisted metric.
    """
    metric = Metric(name=name, unit=unit)
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric


def get(db: Session, metric_id: int) -> Metric | None:
    """Retrieve a single metric by ID.

    Args:
        db: Database session.
        metric_id: The ID of the metric to retrieve.

    Returns:
        The matching metric, or None if it does not exist.
    """
    return db.get(Metric, metric_id)


def delete(db: Session, metric: Metric) -> None:
    """Delete a metric.

    Args:
        db: Database session.
        metric: The metric to delete.
    """
    db.delete(metric)
    db.commit()
