from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.dependencies import get_current_user
from src.models import Metric, User
from src.repositories import metric_repository
from src.schemas.metric import MetricCreate, MetricRead

router = APIRouter(prefix="/metrics", tags=["metrics"])

NOT_FOUND_RESPONSE = {404: {"description": "Metric not found"}}


@router.post("", response_model=MetricRead, status_code=201)
def create_metric(
    payload: MetricCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Metric:
    """Create a new Metric with the given name and unit"""
    return metric_repository.create(db, payload.name, payload.unit)
