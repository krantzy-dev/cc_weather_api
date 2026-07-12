from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Measurement
from src.repositories import location_repository, measurement_repository
from src.schemas.measurement import MeasurementRead

router = APIRouter(tags=["measurements"])


@router.get(
    "/locations/{location_id}/measurements",
    response_model=list[MeasurementRead],
    responses={404: {"description": "Location not found"}},
)
def list_measurements(
    location_id: int,
    from_: datetime | None = Query(None, alias="from"),
    to: datetime | None = Query(None),
    metric_id: int | None = Query(None),
    min_horizon: int | None = Query(None, ge=0),
    n_forecasts: int | None = Query(None, ge=1),
    db: Session = Depends(get_db),
) -> list[Measurement]:
    """List measurements for a location, with optional filters.

    `from` and `to` restrict the timestamp (`ts_value`) range. `metric_id`
    restricts to a single metric. `min_horizon` requires a minimum forecast
    horizon in hours. `n_forecasts` keeps, per timestamp and metric, only the
    N forecasts with the smallest horizon that still satisfy `min_horizon`.
    """
    if location_repository.get(db, location_id) is None:
        raise HTTPException(status_code=404, detail="location not found")

    return measurement_repository.list_for_location(
        db,
        location_id=location_id,
        ts_from=from_,
        ts_to=to,
        metric_id=metric_id,
        min_horizon=min_horizon,
        n_forecasts=n_forecasts,
    )


@router.get(
    "/locations/{location_id}/measurements/latest",
    response_model=list[MeasurementRead],
    responses={404: {"description": "Location not found"}},
)
def latest_measurements(location_id: int, db: Session = Depends(get_db)) -> list[Measurement]:
    """Return the most recent actual (non-forecast) measurement per metric."""
    if location_repository.get(db, location_id) is None:
        raise HTTPException(status_code=404, detail="location not found")

    return measurement_repository.get_latest_for_location(db, location_id)


@router.get("/measurements", response_model=list[MeasurementRead])
def list_measurements_by_ts(
    ts: datetime = Query(...), db: Session = Depends(get_db)
) -> list[Measurement]:
    """List all measurements across all locations for an exact timestamp."""
    return measurement_repository.list_by_ts(db, ts)
