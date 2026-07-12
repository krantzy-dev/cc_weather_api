from src.models import Location


def test_create_location_returns_created_resource(authenticated_client):
    """POST /locations should return the newly created location with an ID."""
    response = authenticated_client.post(
        "/locations",
        json={"name": "Bir Tawil", "lat": 21.8710, "lon": 33.7511},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Bir Tawil"
    assert body["lat"] == 21.8710
    assert body["lon"] == 33.7511
    assert "id" in body
    assert "created" in body


def test_locations_do_not_leak_between_tests(client):
    """Verify test isolation: no location from a previous test should exist here."""
    response = client.get("/locations")
    assert response.json() == []


def test_list_locations_returns_seeded_data(seeded_client):
    """GET /locations should return all seeded locations."""
    response = seeded_client.get("/locations")

    assert response.status_code == 200
    names = {loc["name"] for loc in response.json()}
    assert names == {"Point Nemo", "McMurdo Station"}


def test_get_location_by_id(seeded_client, seeded_db):
    """GET /locations/{id} should return the matching seeded location."""
    location = seeded_db.query(Location).filter_by(name="Point Nemo").one()

    response = seeded_client.get(f"/locations/{location.id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Point Nemo"


def test_get_location_not_found(client):
    """GET /locations/{id} should 404 for a non-existent ID."""
    response = client.get("/locations/999")
    assert response.status_code == 404


def test_update_location_name(seed_authenticated_client, seeded_db):
    """PATCH /locations/{id} should update the location's name."""
    location = seeded_db.query(Location).filter_by(name="Point Nemo").one()

    response = seed_authenticated_client.patch(
        f"/locations/{location.id}", json={"name": "Point Nemo Renamed"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Point Nemo Renamed"


def test_update_location_not_found(authenticated_client):
    """PATCH /locations/{id} should 404 for a non-existent ID."""
    response = authenticated_client.patch("/locations/999", json={"name": "does not matter"})
    assert response.status_code == 404


def test_delete_location(seed_authenticated_client, seeded_db):
    """DELETE /locations/{id} should remove the location."""
    location = seeded_db.query(Location).filter_by(name="McMurdo Station").one()

    response = seed_authenticated_client.delete(f"/locations/{location.id}")
    assert response.status_code == 204

    follow_up = seed_authenticated_client.get(f"/locations/{location.id}")
    assert follow_up.status_code == 404


def test_delete_location_not_found(authenticated_client):
    """DELETE /locations/{id} should 404 for a non-existent ID."""
    response = authenticated_client.delete("/locations/999")
    assert response.status_code == 404
