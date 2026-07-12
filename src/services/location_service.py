import math

from src.exceptions import LocationTooCloseError

EARTH_RADIUS_KM = 6371.0
MIN_LOCATION_DISTANCE_KM = 1.0


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two coordinates in km.

    Args:
        lat1: Latitude of the first point, in decimal degrees.
        lon1: Longitude of the first point, in decimal degrees.
        lat2: Latitude of the second point, in decimal degrees.
        lon2: Longitude of the second point, in decimal degrees.

    Returns:
        The distance between the two points in kilometers.
    """
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def ensure_location_is_far_enough(
    lat: float,
    lon: float,
    existing_coordinates: list[tuple[float, float]],
    min_distance_km: float = MIN_LOCATION_DISTANCE_KM,
) -> None:
    """Ensure a new location is not too close to any existing location.

    Args:
        lat: Latitude of the candidate location.
        lon: Longitude of the candidate location.
        existing_coordinates: Coordinates of all already existing locations.
        min_distance_km: Minimum required distance to any existing location.

    Raises:
        LocationTooCloseError: If the candidate location is closer than
            `min_distance_km` to any existing location.
    """
    for existing_lat, existing_lon in existing_coordinates:
        distance = haversine_distance_km(lat, lon, existing_lat, existing_lon)
        if distance < min_distance_km:
            raise LocationTooCloseError(distance, min_distance_km)
