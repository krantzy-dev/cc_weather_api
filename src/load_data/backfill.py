from sqlalchemy.orm import Session

from src.load_data.client import fetch_hourly
from src.load_data.parser import parse_hourly_response
from src.repositories import measurement_repository

BACKFILL_PAST_DAYS = 30


def backfill_location(
    db: Session,
    location_id: int,
    lat: float,
    lon: float,
    metric_ids_by_name: dict[str, int],
    forecast_days: int,
) -> int:
    """Fetch and store 30 days of history plus forecast data for a location.

    Args:
        db: Database session.
        location_id: The location to backfill data for.
        lat: Latitude of the location.
        lon: Longitude of the location.
        metric_ids_by_name: Mapping of Open-Meteo variable name to metric_id,
            for every metric currently tracked, in request order.
        forecast_days: Number of forecast days to include going forward.

    Returns:
        The number of measurement rows inserted.
    """
    response = fetch_hourly(
        lat,
        lon,
        list(metric_ids_by_name.keys()),
        past_days=BACKFILL_PAST_DAYS,
        forecast_days=forecast_days,
    )
    rows = parse_hourly_response(response, metric_ids_by_name)
    for row in rows:
        row["location_id"] = location_id

    return measurement_repository.bulk_create(db, rows)


def backfill_metric(
    db: Session,
    metric_id: int,
    metric_name: str,
    locations: list[tuple[int, float, float]],
    forecast_days: int,
) -> int:
    """Fetch and store history plus forecast data for one metric, across all locations.

    Args:
        db: Database session.
        metric_id: The metric to backfill data for.
        metric_name: The Open-Meteo variable name for this metric.
        locations: (location_id, lat, lon) tuples for every existing location.
        forecast_days: Number of forecast days to include going forward.

    Returns:
        The total number of measurement rows inserted, across all locations.
    """
    total_inserted = 0
    for location_id, lat, lon in locations:
        response = fetch_hourly(
            lat,
            lon,
            [metric_name],
            past_days=BACKFILL_PAST_DAYS,
            forecast_days=forecast_days,
        )
        rows = parse_hourly_response(response, {metric_name: metric_id})
        for row in rows:
            row["location_id"] = location_id

        total_inserted += measurement_repository.bulk_create(db, rows)

    return total_inserted
