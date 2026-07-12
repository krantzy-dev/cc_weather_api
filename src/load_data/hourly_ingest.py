import logging

from src.database import SessionLocal
from src.load_data.client import fetch_hourly
from src.load_data.parser import parse_hourly_response
from src.repositories import location_repository, measurement_repository, metric_repository

logger = logging.getLogger(__name__)


def run_hourly_ingest() -> None:
    """Fetch the current hour's value for every location/metric pair.

    Only the single most recent, already-elapsed hour is kept from each
    response; everything else the API returns alongside it is discarded.
    """
    db = SessionLocal()
    try:
        locations = location_repository.list_with_coordinates(db)
        metric_ids_by_name = metric_repository.get_ids_by_name(db)

        if not locations or not metric_ids_by_name:
            logger.info("no locations or metrics configured, skipping hourly ingest")
            return

        all_rows = []
        for location_id, lat, lon in locations:
            response = fetch_hourly(
                lat, lon, list(metric_ids_by_name.keys()), past_days=0, forecast_days=1
            )
            rows = parse_hourly_response(response, metric_ids_by_name)
            current_hour_rows = [row for row in rows if row["forecast_horizon"] == 0]

            for row in current_hour_rows:
                row["location_id"] = location_id
            all_rows.extend(current_hour_rows)

        count = measurement_repository.upsert_many(db, all_rows)
        logger.info("hourly ingest complete: %d rows upserted", count)
    finally:
        db.close()


if __name__ == "__main__":
    from src.logging_config import setup_logging

    setup_logging()
    run_hourly_ingest()
