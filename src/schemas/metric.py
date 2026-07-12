from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MetricCreate(BaseModel):
    """Payload for creating a newa Metric

    Attributes:
        name: Name of the measurement
        unit: Unit the measurement is saved in
    """

    name: str
    unit: str


class MetricRead(BaseModel):
    """Representation of a metric returned by the API

    Attributes:
        id: Unique identifier assigned by the database.
        name: Name for the metric.
        unit: Unit of the mertric
        created: Timestamp of when the metric was created.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    unit: str
    created: datetime
