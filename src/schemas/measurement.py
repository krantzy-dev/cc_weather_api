from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MeasurementRead(BaseModel):
    """Representation of a measurement or forecast as returned by the API.

    Attributes:
        id: Unique identifier assigned by the database.
        location_id: The location this measurement belongs to.
        metric_id: The metric this measurement belongs to.
        ts_value: The timestamp the value applies to (observed or forecast for).
        ts_created: The timestamp the value was retrieved or generated.
        forecast_horizon: Hours between ts_created and ts_value; 0 for
            actually observed measurements.
        value: The measured or forecasted value.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    location_id: int
    metric_id: int
    ts_value: datetime
    ts_created: datetime
    forecast_horizon: int
    value: float
