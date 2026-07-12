import openmeteo_requests

from src.config import settings
from src.exceptions import UnsupportedMetricError

# Common Open-Meteo hourly variables (api.open-meteo.com/en/docs). Not
# exhaustive, extend as needed if you start tracking additional metrics.
SUPPORTED_HOURLY_VARIABLES = {
    "temperature_2m",
    "relative_humidity_2m",
    "dew_point_2m",
    "apparent_temperature",
    "precipitation",
    "rain",
    "showers",
    "snowfall",
    "snow_depth",
    "weather_code",
    "pressure_msl",
    "surface_pressure",
    "cloud_cover",
    "cloud_cover_low",
    "cloud_cover_mid",
    "cloud_cover_high",
    "visibility",
    "evapotranspiration",
    "et0_fao_evapotranspiration",
    "vapour_pressure_deficit",
    "wind_speed_10m",
    "wind_speed_80m",
    "wind_direction_10m",
    "wind_gusts_10m",
    "soil_temperature_0cm",
    "soil_moisture_0_to_1cm",
    "is_day",
    "sunshine_duration",
    "uv_index",
}

# Used only to probe whether a metric name is accepted by the API. Location itself is irrelevant.
_PROBE_LATITUDE = 0.0
_PROBE_LONGITUDE = 0.0


def _validate_format(name: str) -> None:
    """Check a metric name against the static list of known variables.

    Args:
        name: The metric name to validate.

    Raises:
        UnsupportedMetricError: If the name is not in the static list.
    """
    if name not in SUPPORTED_HOURLY_VARIABLES:
        raise UnsupportedMetricError(name, "not in the list of known Open-Meteo variables")


def _validate_live(name: str) -> None:
    """Confirm a metric name is accepted by the live Open-Meteo API.

    Args:
        name: The metric name to validate.

    Raises:
        UnsupportedMetricError: If the API rejects the name.
    """
    client = openmeteo_requests.Client()
    try:
        client.weather_api(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": _PROBE_LATITUDE,
                "longitude": _PROBE_LONGITUDE,
                "hourly": [name],
                "forecast_days": 1,
            },
        )
    except Exception as exc:
        raise UnsupportedMetricError(name, str(exc)) from exc


def validate_metric_name(name: str) -> None:
    """Validate a metric name against the static list, and live if enabled.

    Args:
        name: The metric name to validate.

    Raises:
        UnsupportedMetricError: If the name fails either check.
    """
    _validate_format(name)
    if settings.online:
        _validate_live(name)
