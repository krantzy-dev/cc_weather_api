from src.models import Location


def _location_id(seeded_db, name: str) -> int:
    return seeded_db.query(Location).filter_by(name=name).one().id


def test_list_measurements_returns_all_for_location(seeded_client, seeded_db):
    """No filters: all measurements (both metrics, all horizons) for the location."""
    location_id = _location_id(seeded_db, "Point Nemo")

    response = seeded_client.get(f"/locations/{location_id}/measurements")

    assert response.status_code == 200
    assert len(response.json()) == 7  # 5 temperature_2m + 2 cloud_cover


def test_list_measurements_filters_by_metric(seeded_client, seeded_db):
    """metric_id filter restricts to a single metric."""
    location_id = _location_id(seeded_db, "Point Nemo")
    metric_response = seeded_client.get("/metrics")
    temp_metric_id = next(m["id"] for m in metric_response.json() if m["name"] == "temperature_2m")

    response = seeded_client.get(
        f"/locations/{location_id}/measurements", params={"metric_id": temp_metric_id}
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 5
    assert all(m["metric_id"] == temp_metric_id for m in body)


def test_list_measurements_filters_by_min_horizon(seeded_client, seeded_db):
    """min_horizon keeps only measurements with forecast_horizon >= given value."""
    location_id = _location_id(seeded_db, "Point Nemo")

    response = seeded_client.get(
        f"/locations/{location_id}/measurements", params={"min_horizon": 12}
    )

    assert response.status_code == 200
    horizons = {m["forecast_horizon"] for m in response.json()}
    assert horizons == {12, 24}


def test_list_measurements_filters_by_n_forecasts(seeded_client, seeded_db):
    """n_forecasts keeps, per (ts_value, metric), only the N smallest horizons
    among those already satisfying min_horizon."""
    location_id = _location_id(seeded_db, "Point Nemo")

    response = seeded_client.get(
        f"/locations/{location_id}/measurements",
        params={"min_horizon": 6, "n_forecasts": 1},
    )

    assert response.status_code == 200
    body = response.json()
    # Two (ts_value, metric) groups satisfy min_horizon=6: temperature_2m/14:00
    # (horizons 6, 12, 24 qualify) and cloud_cover/14:00 (horizon 6 qualifies).
    # n_forecasts=1 keeps exactly the smallest qualifying horizon per group.
    assert len(body) == 2
    horizons_by_metric_id = {m["metric_id"]: m["forecast_horizon"] for m in body}
    assert set(horizons_by_metric_id.values()) == {6}


def test_list_measurements_filters_by_n_forecasts_keeps_smallest_n(seeded_client, seeded_db):
    """With n_forecasts=2, the temperature_2m group keeps horizons 6 and 12
    (the two smallest that satisfy min_horizon=6), not 12 and 24."""
    location_id = _location_id(seeded_db, "Point Nemo")
    metrics_response = seeded_client.get("/metrics")
    temp_metric_id = next(m["id"] for m in metrics_response.json() if m["name"] == "temperature_2m")

    response = seeded_client.get(
        f"/locations/{location_id}/measurements",
        params={"metric_id": temp_metric_id, "min_horizon": 6, "n_forecasts": 2},
    )

    assert response.status_code == 200
    horizons = sorted(m["forecast_horizon"] for m in response.json())
    assert horizons == [6, 12]


def test_list_measurements_filters_by_time_range(seeded_client, seeded_db):
    """from/to restrict the ts_value range."""
    location_id = _location_id(seeded_db, "Point Nemo")

    response = seeded_client.get(
        f"/locations/{location_id}/measurements",
        params={"from": "2026-06-08T14:30:00+00:00", "to": "2026-06-08T16:00:00+00:00"},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["ts_value"].startswith("2026-06-08T15:00:00")


def test_list_measurements_location_not_found(client):
    """404 for a non-existent location."""
    response = client.get("/locations/999/measurements")
    assert response.status_code == 404


def test_latest_measurements_returns_highest_ts_value_per_metric(seeded_client, seeded_db):
    """latest returns, per metric, the horizon=0 entry with the highest ts_value."""
    location_id = _location_id(seeded_db, "Point Nemo")

    response = seeded_client.get(f"/locations/{location_id}/measurements/latest")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2  # one per metric

    values_by_metric_name = {}
    metrics_response = seeded_client.get("/metrics")
    metric_names = {m["id"]: m["name"] for m in metrics_response.json()}
    for m in body:
        values_by_metric_name[metric_names[m["metric_id"]]] = m

    # temperature_2m's latest horizon=0 entry is at 15:00, not 14:00
    assert values_by_metric_name["temperature_2m"]["ts_value"].startswith("2026-06-08T15:00:00")
    assert values_by_metric_name["temperature_2m"]["value"] == 18.6
    # cloud_cover only has a horizon=0 entry at 14:00
    assert values_by_metric_name["cloud_cover"]["value"] == 42


def test_latest_measurements_location_not_found(client):
    """404 for a non-existent location."""
    response = client.get("/locations/999/measurements/latest")
    assert response.status_code == 404


def test_list_measurements_by_ts_spans_locations(seeded_client):
    """The global ts filter returns matching measurements across all locations."""
    response = seeded_client.get("/measurements", params={"ts": "2026-06-08T14:00:00+00:00"})

    assert response.status_code == 200
    body = response.json()
    # Point Nemo: 4 temperature_2m + 2 cloud_cover, McMurdo: 2 temperature_2m
    assert len(body) == 8


def test_list_measurements_by_ts_no_match_returns_empty(seeded_client):
    """A timestamp with no matching measurements returns an empty list."""
    response = seeded_client.get("/measurements", params={"ts": "2020-01-01T00:00:00+00:00"})

    assert response.status_code == 200
    assert response.json() == []
