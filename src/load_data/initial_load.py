import logging

from sqlalchemy.orm import Session

from src.config import settings
from src.load_data.backfill import backfill_location
from src.repositories import location_repository, metric_repository

logger = logging.getLogger(__name__)

INITIAL_METRICS = [
    ("temperature_2m", "°C"),
    ("rain", "mm"),
]

INITIAL_LOCATION = {"name": "CERN Geneva", "lat": 46.2044, "lon": 6.0483}


def run_initial_load(db: Session) -> None:
    """Seed an initial metric set and location, if the database is empty.

    Skipped entirely if a location already exists (idempotent across
    restarts), or if ONLINE is disabled (backfilling requires network
    access to Open-Meteo).

    Args:
        db: Database session.
    """
    if not settings.online:
        logger.info("ONLINE=false, skipping initial data load")
        return

    if location_repository.list_all(db):
        logger.info("locations already exist, skipping initial data load")
        return

    for name, unit in INITIAL_METRICS:
        if metric_repository.get_by_name(db, name) is None:
            metric_repository.create(db, name, unit)

    location = location_repository.create(
        db, INITIAL_LOCATION["name"], INITIAL_LOCATION["lat"], INITIAL_LOCATION["lon"]
    )

    metric_ids_by_name = metric_repository.get_ids_by_name(db)
    backfill_location(
        db, location.id, location.lat, location.lon, metric_ids_by_name, settings.forecast_days
    )

    logger.info("initial data load complete: location '%s' created and backfilled", location.name)
