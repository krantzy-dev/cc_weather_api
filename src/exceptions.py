class LocationTooCloseError(Exception):
    """Raised when a new location is too close to an already existing one."""

    def __init__(self, distance_km: float, min_distance_km: float) -> None:
        self.distance_km = distance_km
        self.min_distance_km = min_distance_km
        super().__init__(f"location is {distance_km:.2f}km away, minimum is {min_distance_km}km")


class EmailAlreadyRegisteredError(Exception):
    """Raised when attempting to register an email that already exists."""

    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"email '{email}' is already registered")


class InvalidCredentialsError(Exception):
    """Raised when login credentials do not match any user."""


class InvalidTokenError(Exception):
    """Raised when a bearer token is missing, malformed, or expired."""
