from datetime import datetime

from sqlalchemy import and_, func, insert, select
from sqlalchemy.orm import Session, aliased

from src.models import Measurement


def list_for_location(
    db: Session,
    location_id: int,
    ts_from: datetime | None = None,
    ts_to: datetime | None = None,
    metric_id: int | None = None,
    min_horizon: int | None = None,
    n_forecasts: int | None = None,
) -> list[Measurement]:
    """List measurements for a location, with optional filters.

    Args:
        db: Database session.
        location_id: The location to list measurements for.
        ts_from: Minimum ts_value (inclusive), if filtering by time range.
        ts_to: Maximum ts_value (inclusive), if filtering by time range.
        metric_id: Restrict to a single metric, if given.
        min_horizon: Minimum forecast_horizon (inclusive), if given.
        n_forecasts: If given, keep only the N forecasts with the smallest
            horizon (among those already satisfying min_horizon) per
            (ts_value, metric_id) pair.

    Returns:
        The matching measurements, ordered by ts_value, metric_id, and
        forecast_horizon.
    """
    conditions = [Measurement.location_id == location_id]
    if ts_from is not None:
        conditions.append(Measurement.ts_value >= ts_from)
    if ts_to is not None:
        conditions.append(Measurement.ts_value <= ts_to)
    if metric_id is not None:
        conditions.append(Measurement.metric_id == metric_id)
    if min_horizon is not None:
        conditions.append(Measurement.forecast_horizon >= min_horizon)

    if n_forecasts is None:
        stmt = (
            select(Measurement)
            .where(and_(*conditions))
            .order_by(Measurement.ts_value, Measurement.metric_id, Measurement.forecast_horizon)
        )
        return db.execute(stmt).scalars().all()

    row_number = (
        func.row_number()
        .over(
            partition_by=(Measurement.ts_value, Measurement.metric_id),
            order_by=Measurement.forecast_horizon.asc(),
        )
        .label("row_number")
    )
    subquery = select(Measurement, row_number).where(and_(*conditions)).subquery()
    ranked = aliased(Measurement, subquery)

    stmt = (
        select(ranked)
        .where(subquery.c.row_number <= n_forecasts)
        .order_by(subquery.c.ts_value, subquery.c.metric_id, subquery.c.forecast_horizon)
    )
    return db.execute(stmt).scalars().all()


def get_latest_for_location(db: Session, location_id: int) -> list[Measurement]:
    """Return the most recent actual (non-forecast) measurement per metric.

    Args:
        db: Database session.
        location_id: The location to retrieve latest measurements for.

    Returns:
        One measurement per metric: the one with the highest ts_value among
        those with forecast_horizon == 0.
    """
    conditions = [Measurement.location_id == location_id, Measurement.forecast_horizon == 0]

    row_number = (
        func.row_number()
        .over(partition_by=Measurement.metric_id, order_by=Measurement.ts_value.desc())
        .label("row_number")
    )
    subquery = select(Measurement, row_number).where(and_(*conditions)).subquery()
    ranked = aliased(Measurement, subquery)

    stmt = select(ranked).where(subquery.c.row_number == 1)
    return db.execute(stmt).scalars().all()


def list_by_ts(db: Session, ts_value: datetime) -> list[Measurement]:
    """List all measurements across all locations for an exact timestamp.

    Args:
        db: Database session.
        ts_value: The exact timestamp to filter by.

    Returns:
        All measurements with a matching ts_value, across every location.
    """
    stmt = (
        select(Measurement)
        .where(Measurement.ts_value == ts_value)
        .order_by(Measurement.location_id, Measurement.metric_id, Measurement.forecast_horizon)
    )
    return db.execute(stmt).scalars().all()


def bulk_create(db: Session, rows: list[dict]) -> int:
    """Bulk insert measurement rows.

    Args:
        db: Database session.
        rows: Dicts with location_id, metric_id, ts_value, ts_created,
            forecast_horizon, and value.

    Returns:
        The number of rows inserted.
    """
    if not rows:
        return 0
    db.execute(insert(Measurement), rows)
    db.commit()
    return len(rows)
