from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import Location


def list_coordinates(db: Session) -> list[tuple[float, float]]:
    """Retrieve the coordinates of all existing locations.

    Args:
        db: Database session.

    Returns:
        A list of (lat, lon) tuples for every existing location.
    """
    rows = db.execute(select(Location.lat, Location.lon)).all()
    return [(row.lat, row.lon) for row in rows]


def create(db: Session, name: str, lat: float, lon: float) -> Location:
    """Insert a new location.

    Args:
        db: Database session.
        name: Human-readable label for the location.
        lat: Latitude in decimal degrees.
        lon: Longitude in decimal degrees.

    Returns:
        The newly created, persisted location.
    """
    location = Location(name=name, lat=lat, lon=lon)
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def get(db: Session, location_id: int) -> Location | None:
    """Retrieve a single location by ID.

    Args:
        db: Database session.
        location_id: The ID of the location to retrieve.

    Returns:
        The matching location, or None if it does not exist.
    """
    return db.get(Location, location_id)


def list_all(db: Session) -> list[Location]:
    """Retrieve all locations.

    Args:
        db: Database session.

    Returns:
        Every location currently stored.
    """
    return db.execute(select(Location)).scalars().all()


def update_name(db: Session, location: Location, name: str) -> Location:
    """Update a location's name.

    Args:
        db: Database session.
        location: The location to update.
        name: The new name.

    Returns:
        The updated location.
    """
    location.name = name
    db.commit()
    db.refresh(location)
    return location


def delete(db: Session, location: Location) -> None:
    """Delete a location.

    Args:
        db: Database session.
        location: The location to delete.
    """
    db.delete(location)
    db.commit()
