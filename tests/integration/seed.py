import json

from sqlalchemy.orm import Session

from src.config import settings
from src.models import Location, Measurement, Metric, User

SEED_DATA_PATH = settings.root_dir.joinpath("tests/integration/fixtures/seed_data.json")


def load_seed_data(session: Session) -> None:
    """Insert the shared seed dataset into the given session."""
    with open(SEED_DATA_PATH) as f:
        data = json.load(f)

    for user_data in data["users"]:
        session.add(User(**user_data))

    locations = {loc["name"]: Location(**loc) for loc in data["locations"]}
    metrics = {m["name"]: Metric(**m) for m in data["metrics"]}
    session.add_all([*locations.values(), *metrics.values()])

    session.flush()  # assigns auto-increment IDs without ending the transaction

    for m in data["measurements"]:
        session.add(
            Measurement(
                location_id=locations[m["location"]].id,
                metric_id=metrics[m["metric"]].id,
                ts_value=m["ts_value"],
                ts_created=m["ts_created"],
                forecast_horizon=m["forecast_horizon"],
                value=m["value"],
            )
        )

    session.flush()
