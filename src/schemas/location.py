from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LocationCreate(BaseModel):
    """Payload for creating a new location.

    Attributes:
        name: Human-readable name for the location.
        lat: Latitude in decimal degrees.
        lon: Longitude in decimal degrees.
    """

    name: str
    lat: float
    lon: float


class LocationUpdate(BaseModel):
    """Payload for updating a location.

    Only the name can be changed. Latitude and longitude are immutable by
    design: changing the coordinates of a location would conceptually make
    it a different location, not an update to the existing one.

    Attributes:
        name: The new name for the location.
    """

    name: str


class LocationRead(BaseModel):
    """Representation of a location returned by the API.

    Attributes:
        id: Unique identifier assigned by the database.
        name: Human-readable name for the location.
        lat: Latitude in decimal degrees.
        lon: Longitude in decimal degrees.
        created: Timestamp of when the location was created.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    lat: float
    lon: float
    created: datetime
