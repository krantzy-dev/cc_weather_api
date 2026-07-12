# tests/unit/test_location_service.py
import pytest

from src.exceptions import LocationTooCloseError
from src.services.location_service import ensure_location_is_far_enough, haversine_distance_km


def test_haversine_distance_known_points():
    """Berlin to Hamburg is roughly 255km, sanity-check the formula."""
    distance = haversine_distance_km(52.5200, 13.4050, 53.5511, 9.9937)
    assert 250 < distance < 260


def test_ensure_location_is_far_enough_passes_when_no_conflicts():
    """No error should be raised when far away from all existing locations."""
    ensure_location_is_far_enough(
        lat=-48.8767, lon=-123.3933, existing_coordinates=[(-77.8419, 166.6863)]
    )


def test_ensure_location_is_far_enough_raises_when_too_close():
    """An error should be raised when within the minimum distance."""
    with pytest.raises(LocationTooCloseError):
        ensure_location_is_far_enough(
            lat=-48.8767,
            lon=-123.3933,
            existing_coordinates=[(-48.8768, -123.3934)],
            min_distance_km=1.0,
        )
