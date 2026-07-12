from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Location
from src.schemas.location import LocationCreate, LocationRead, LocationUpdate

router = APIRouter(prefix="/locations", tags=["locations"])


@router.post("", response_model=LocationRead, status_code=201)
def create_location(payload: LocationCreate, db: Session = Depends(get_db)) -> Location:
    """Create a new location with the given name and coordinates."""
    location = Location(**payload.model_dump())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


@router.get("", response_model=list[LocationRead])
def list_locations(db: Session = Depends(get_db)) -> list[Location]:
    """List all locations currently stored."""
    return db.execute(select(Location)).scalars().all()


@router.get("/{location_id}", response_model=LocationRead)
def get_location(location_id: int, db: Session = Depends(get_db)) -> Location:
    """Retrieve a single location by its ID."""
    location = db.get(Location, location_id)
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
    location = db.get(Location, location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="location not found")

    location.name = payload.name
    db.commit()
    db.refresh(location)
    return location


@router.delete("/{location_id}", status_code=204)
def delete_location(location_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a location.

    Associated measurements are not currently deleted along with the
    location. Cascading deletion will be added once data ingestion is
    implemented.
    """
    location = db.get(Location, location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="location not found")

    db.delete(location)
    db.commit()
