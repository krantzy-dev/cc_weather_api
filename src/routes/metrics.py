from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config import settings
from src.database import get_db
from src.dependencies import get_current_user
from src.exceptions import MetricAlreadyExistsError
from src.load_data.backfill import backfill_metric
from src.models import Metric, User
from src.repositories import location_repository, metric_repository
from src.schemas.metric import MetricCreate, MetricRead
from src.services.metric_validation import validate_metric_name

router = APIRouter(prefix="/metrics", tags=["metrics"])

NOT_FOUND_RESPONSE = {404: {"description": "Metric not found"}}


@router.post(
    "",
    response_model=MetricRead,
    status_code=201,
    responses={
        409: {"description": "Metric already exists"},
        422: {"description": "Metric name not supported by Open-Meteo"},
    },
)
def create_metric(
    payload: MetricCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Metric:
    """Create a new Metric with the given name and unit"""
    validate_metric_name(payload.name)

    if metric_repository.get_by_name(db, payload.name) is not None:
        raise MetricAlreadyExistsError(payload.name)

    metric = metric_repository.create(db, payload.name, payload.unit)

    locations = location_repository.list_with_coordinates(db)
    if locations:
        backfill_metric(db, metric.id, metric.name, locations, settings.forecast_days)

    return metric


@router.get("", response_model=list[MetricRead])
def list_metrics(db: Session = Depends(get_db)) -> list[Metric]:
    """List all metrics currently stored."""
    return metric_repository.list_all(db)


@router.delete("/{metric_id}", status_code=204, responses=NOT_FOUND_RESPONSE)
def delete_metric(
    metric_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> None:
    """Delete a Metric.

    Associated measurements are not currently deleted along with the
    metric. Cascading deletion will be added once data ingestion is
    implemented.
    """
    metric = metric_repository.get(db, metric_id=metric_id)
    if metric is None:
        raise HTTPException(status_code=404, detail="metric not found")
    metric_repository.delete(db, metric)
