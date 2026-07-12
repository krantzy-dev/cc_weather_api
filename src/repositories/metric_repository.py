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


def get_by_name(db: Session, name: str) -> Metric | None:
    """Retrieve a metric by its exact name.

    Args:
        db: Database session.
        name: The metric name to look up.

    Returns:
        The matching metric, or None if no such metric exists.
    """
    return db.execute(select(Metric).where(Metric.name == name)).scalar_one_or_none()


def get_ids_by_name(db: Session) -> dict[str, int]:
    """Retrieve a mapping of metric name to metric_id for all existing metrics.

    Args:
        db: Database session.

    Returns:
        A dict mapping each metric's name to its ID.
    """
    rows = db.execute(select(Metric.name, Metric.id)).all()
    return {row.name: row.id for row in rows}
