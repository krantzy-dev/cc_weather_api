import logging

from src.config import settings
from src.database import SessionLocal
from src.load_data.client import fetch_hourly
from src.load_data.parser import parse_hourly_response
from src.repositories import location_repository, measurement_repository, metric_repository

logger = logging.getLogger(__name__)


def run_daily_forecast_ingest() -> None:
    """Fetch forecast data for the next FORECAST_DAYS days, for every location/metric pair.

    Only forecast rows (forecast_horizon > 0) are kept; the current hour's
    actual value is handled separately by the hourly ingest job. Each day's
    run preserves its own ts_created, building up forecast history over time.
    """
    db = SessionLocal()
    try:
        locations = location_repository.list_with_coordinates(db)
        metric_ids_by_name = metric_repository.get_ids_by_name(db)

        if not locations or not metric_ids_by_name:
            logger.info("no locations or metrics configured, skipping daily forecast ingest")
            return

        all_rows = []
        for location_id, lat, lon in locations:
            response = fetch_hourly(
                lat,
                lon,
                list(metric_ids_by_name.keys()),
                past_days=0,
                forecast_days=settings.forecast_days,
            )
            rows = parse_hourly_response(response, metric_ids_by_name)
            forecast_rows = [row for row in rows if row["forecast_horizon"] > 0]

            for row in forecast_rows:
                row["location_id"] = location_id
            all_rows.extend(forecast_rows)

        count = measurement_repository.upsert_many(db, all_rows)
        logger.info("daily forecast ingest complete: %d rows upserted", count)
    finally:
        db.close()


if __name__ == "__main__":
    from src.logging_config import setup_logging

    setup_logging()
    run_daily_forecast_ingest()
