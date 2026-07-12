from src.models import Metric


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


def test_delete_metric(seed_authenticated_client, seeded_db):
    """DELETE /metrics/{id} should remove the metric."""
    metric = seeded_db.query(Metric).filter_by(name="temperature_2m").one()

    response = seed_authenticated_client.delete(f"/metrics/{metric.id}")
    assert response.status_code == 204


def test_delete_metric_not_found(authenticated_client):
    """DELETE /metrics/{id} should 404 for a non-existent ID."""
    response = authenticated_client.delete("/metrics/999")
    assert response.status_code == 404


def test_create_metric_rejects_unsupported_name(authenticated_client):
    """POST /metrics should reject a name that isn't a real Open-Meteo variable."""
    response = authenticated_client.post(
        "/metrics", json={"name": "definitely_not_a_real_metric", "unit": "n/a"}
    )
    assert response.status_code == 422
