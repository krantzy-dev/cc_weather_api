from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Location
from src.repositories import location_repository
from src.schemas.location import LocationCreate, LocationRead, LocationUpdate

router = APIRouter(prefix="/locations", tags=["locations"])


@router.post("", response_model=LocationRead, status_code=201)
def create_location(payload: LocationCreate, db: Session = Depends(get_db)) -> Location:
    """Create a new location with the given name and coordinates."""

    return location_repository.create(db, payload.name, payload.lat, payload.lon)


@router.get("", response_model=list[LocationRead])
def list_locations(db: Session = Depends(get_db)) -> list[Location]:
    """List all locations currently stored."""
    return location_repository.list_all(db)


@router.get("/{location_id}", response_model=LocationRead)
def get_location(location_id: int, db: Session = Depends(get_db)) -> Location:
    """Retrieve a single location by its ID."""
    location = location_repository.get(db, location_id=location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="location not found")
    return location


@router.patch("/{location_id}", response_model=LocationRead)
def update_location(
    location_id: int, payload: LocationUpdate, db: Session = Depends(get_db)
) -> Location:
    """Update a location's name.

    Coordinates cannot be changed through this endpoint. Changing latitude
    or longitude would conceptually describe a different location, so a new
    location should be created instead.
    """
    location = location_repository.get(db, location_id=location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="location not found")

    return location_repository.update_name(db, location, payload.name)


@router.delete("/{location_id}", status_code=204)
def delete_location(location_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a location.

    Associated measurements are not currently deleted along with the
    location. Cascading deletion will be added once data ingestion is
    implemented.
    """
    location = location_repository.get(db, location_id=location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="location not found")
    location_repository.delete(db, location)
