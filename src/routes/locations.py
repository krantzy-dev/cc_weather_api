from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config import settings
from src.database import get_db
from src.dependencies import get_current_user
from src.load_data.backfill import backfill_location
from src.models import Location, User
from src.repositories import location_repository, metric_repository
from src.schemas.location import LocationCreate, LocationRead, LocationUpdate
from src.services.location_service import ensure_location_is_far_enough

router = APIRouter(prefix="/locations", tags=["locations"])

NOT_FOUND_RESPONSE = {404: {"description": "Location not found"}}


@router.post(
    "",
    response_model=LocationRead,
    status_code=201,
    responses={409: {"description": "Location too close to an existing one"}},
)
def create_location(
    payload: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Location:
    """Create a new location with the given name and coordinates."""
    existing_coordinates = location_repository.list_coordinates(db)
    ensure_location_is_far_enough(payload.lat, payload.lon, existing_coordinates)

    location = location_repository.create(db, payload.name, payload.lat, payload.lon)

    metric_ids_by_name = metric_repository.get_ids_by_name(db)
    if metric_ids_by_name:
        backfill_location(
            db,
            location.id,
            location.lat,
            location.lon,
            metric_ids_by_name,
            settings.forecast_days,
        )

    return location


@router.get("", response_model=list[LocationRead])
def list_locations(db: Session = Depends(get_db)) -> list[Location]:
    """List all locations currently stored."""
    return location_repository.list_all(db)


@router.get("/{location_id}", response_model=LocationRead, responses=NOT_FOUND_RESPONSE)
def get_location(location_id: int, db: Session = Depends(get_db)) -> Location:
    """Retrieve a single location by its ID."""
    location = location_repository.get(db, location_id=location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="location not found")
    return location


@router.patch("/{location_id}", response_model=LocationRead, responses=NOT_FOUND_RESPONSE)
def update_location(
    location_id: int,
    payload: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Location:
    """Update a location's name.

    Will trigger a cascading delete in measurements
    """
    location = location_repository.get(db, location_id=location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="location not found")

    return location_repository.update_name(db, location, payload.name)


@router.delete("/{location_id}", status_code=204, responses=NOT_FOUND_RESPONSE)
def delete_location(
    location_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> None:
    """Delete a location.

    Will trigger a cascading delete in measurements
    """
    location = location_repository.get(db, location_id=location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="location not found")
    location_repository.delete(db, location)
