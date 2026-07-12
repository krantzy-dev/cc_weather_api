def test_create_metric_returns_created_resource(authenticated_client):
    """POST /metrics should return the newly created metric with an ID."""
    response = authenticated_client.post(
        "/metrics",
        json={"name": "air_temp", "unit": "Degrees Celsius"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "air_temp"
    assert body["unit"] == "Degrees Celsius"
    assert "id" in body
    assert "created" in body
