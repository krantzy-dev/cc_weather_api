from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LocationCreate(BaseModel):
    name: str
    lat: float
    lon: float


class LocationUpdate(BaseModel):
    name: str


class LocationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    lat: float
    lon: float
    created: datetime
