def test_create_metric_returns_created_resource(authenticated_client):
    """POST /metrics should return the newly created metric with an ID."""
    response = authenticated_client.post(
        "/metrics",
        json={"name": "temperature_2m", "unit": "°C"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "temperature_2m"
    assert body["unit"] == "°C"
    assert "id" in body
    assert "created" in body


def test_metrics_do_not_leak_between_tests(client):
    """Verify test isolation: no metric from a previous test should exist here."""
    response = client.get("/metrics")
    assert response.json() == []


def test_list_metrics_returns_seeded_data(seeded_client):
    """GET /metrics should return all seeded metrics."""
    response = seeded_client.get("/metrics")

    assert response.status_code == 200
    names = {loc["name"] for loc in response.json()}
    assert names == {"temperature_2m", "cloud_cover"}
