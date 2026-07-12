from datetime import UTC, datetime


def parse_hourly_response(
    response, metric_ids_by_name: dict[str, int], now: datetime | None = None
) -> list[dict]:
    """Parse a raw Open-Meteo hourly response into measurement rows.

    Args:
        response: The raw Open-Meteo response object from fetch_hourly.
        metric_ids_by_name: Mapping from Open-Meteo variable name to metric_id.
        now: The reference time to treat as "current". Defaults to the real
            current time; can be overridden to simulate past ingestion runs.

    Returns:
        A list of dicts, each with keys: metric_id, ts_value, ts_created,
        forecast_horizon, value.
    """
    if now is None:
        now = datetime.now(UTC)
    now = now.replace(minute=0, second=0, microsecond=0)

    hourly = response.Hourly()
    epochs = range(hourly.Time(), hourly.TimeEnd(), hourly.Interval())

    rows = []
    for i, metric_id in enumerate(metric_ids_by_name.values()):
        values = hourly.Variables(i).ValuesAsNumpy()
        for ts_epoch, value in zip(epochs, values, strict=True):
            ts_value = datetime.fromtimestamp(ts_epoch, tz=UTC)

            if ts_value <= now:
                ts_created = ts_value
                forecast_horizon = 0
            else:
                ts_created = now
                forecast_horizon = int((ts_value - ts_created).total_seconds() // 3600)

            rows.append(
                {
                    "metric_id": metric_id,
                    "ts_value": ts_value,
                    "ts_created": ts_created,
                    "forecast_horizon": forecast_horizon,
                    "value": float(value),
                }
            )
    return rows
