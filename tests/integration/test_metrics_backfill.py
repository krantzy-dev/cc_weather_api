import pytest

from src.config import settings
from src.models import Measurement

pytestmark = pytest.mark.skipif(
    not settings.online, reason="ONLINE=false, skipping live Open-Meteo backfill checks"
)


def test_create_metric_backfills_measurements(authenticated_client, db_session):
    """Creating a metric with existing locations should trigger a real backfill."""
    authenticated_client.post(
        "/locations", json={"name": "Bir Tawil", "lat": 21.8710, "lon": 33.7511}
    )

    response = authenticated_client.post("/metrics", json={"name": "cloud_cover", "unit": "%"})
    metric_id = response.json()["id"]

    count = db_session.query(Measurement).filter_by(metric_id=metric_id).count()
    assert count > 0
