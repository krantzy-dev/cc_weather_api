import pytest

from src.config import settings
from src.models import Measurement

pytestmark = pytest.mark.skipif(
    not settings.online, reason="ONLINE=false, skipping live Open-Meteo backfill checks"
)


def test_create_location_backfills_measurements(authenticated_client, db_session):
    """Creating a location with existing metrics should trigger a real backfill."""
    authenticated_client.post("/metrics", json={"name": "temperature_2m", "unit": "°C"})

    response = authenticated_client.post(
        "/locations", json={"name": "Bir Tawil", "lat": 21.8710, "lon": 33.7511}
    )
    location_id = response.json()["id"]

    count = db_session.query(Measurement).filter_by(location_id=location_id).count()
    assert count > 0
