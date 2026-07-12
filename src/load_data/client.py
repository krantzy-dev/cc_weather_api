import openmeteo_requests

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_hourly(lat: float, lon: float, variables: list[str], past_days: int, forecast_days: int):
    """Fetch raw hourly weather data from the Open-Meteo forecast endpoint.

    Args:
        lat: Latitude of the location.
        lon: Longitude of the location.
        variables: Open-Meteo hourly variable names to request, in order.
        past_days: Number of past days to include (0-92).
        forecast_days: Number of forecast days to include (0-16).

    Returns:
        The raw Open-Meteo response object for this location.
    """
    client = openmeteo_requests.Client()
    responses = client.weather_api(
        FORECAST_URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": variables,
            "past_days": past_days,
            "forecast_days": forecast_days,
            "timezone": "UTC",
        },
    )
    return responses[0]
