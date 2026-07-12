import pytest

from src.config import settings
from src.exceptions import UnsupportedMetricError
from src.services.metric_validation import _validate_format

pytestmark = pytest.mark.skipif(
    not settings.online, reason="ONLINE=false, skipping live Open-Meteo checks"
)


def test_validate_format_accepts_known_metric():
    """A known Open-Meteo variable should pass without error."""
    _validate_format("temperature_2m")


def test_validate_format_rejects_unknown_metric():
    """An unknown variable name should be rejected."""
    with pytest.raises(UnsupportedMetricError):
        _validate_format("definitely_not_a_real_metric")
