from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock

from src.load_data.parser import parse_hourly_response


def _make_fake_response(start: datetime, hours: int, values: list[float]):
    fake_hourly = MagicMock()
    fake_hourly.Time.return_value = int(start.timestamp())
    fake_hourly.TimeEnd.return_value = int((start + timedelta(hours=hours)).timestamp())
    fake_hourly.Interval.return_value = 3600

    fake_variable = MagicMock()
    fake_variable.ValuesAsNumpy.return_value = values
    fake_hourly.Variables.return_value = fake_variable

    fake_response = MagicMock()
    fake_response.Hourly.return_value = fake_hourly
    return fake_response


def test_parse_hourly_response_marks_past_as_observed():
    """Timestamps at or before now get forecast_horizon 0 and ts_created == ts_value."""
    now = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)
    past = now - timedelta(hours=2)
    response = _make_fake_response(past, hours=1, values=[18.4])

    rows = parse_hourly_response(response, {"temperature_2m": 1})

    assert len(rows) == 1
    assert rows[0]["forecast_horizon"] == 0
    assert rows[0]["ts_created"] == rows[0]["ts_value"]


def test_parse_hourly_response_marks_future_as_forecast():
    """Timestamps after now get a positive forecast_horizon in hours."""
    now = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)
    future = now + timedelta(hours=6)
    response = _make_fake_response(future, hours=1, values=[19.1])

    rows = parse_hourly_response(response, {"temperature_2m": 1})

    assert len(rows) == 1
    assert rows[0]["forecast_horizon"] == 6
    assert rows[0]["ts_created"] == now
