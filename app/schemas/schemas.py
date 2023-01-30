"""This module contains classes that define schemas for the API."""
from pydantic import BaseModel


class OKMessage(BaseModel):
    """API response for a successful request."""

    class Config:
        """It overrides the default FastAPI example"""

        schema_extra = {"example": "OK"}


class TripBase(BaseModel):
    """Base class for trip data model."""

    region: str
    datetime: str
    datasource: str


class TripCreate(TripBase):
    """Schema for creating trip data."""

    origin_coord: str
    destination_coord: str

    class Config:
        """It overrides the default FastAPI example"""

        schema_extra = {
            "example": {
                "region": "Prague",
                "origin_coord": "POINT (14.4973794438195 50.00136875782316)",
                "destination_coord": "POINT (14.43109483523328 50.04052930943246)",
                "datetime": "2018-05-28 09:03:40",
                "datasource": "funny_car",
            }
        }


class TripGet(TripBase):
    """Schema for retrieving trip data."""

    origin_coord_x: float
    origin_coord_y: float
    destination_coord_x: float
    destination_coord_y: float

    class Config:
        """It overrides the default FastAPI example"""

        schema_extra = {
            "example": {
                "region": "Prague",
                "origin_coord_x": 14.4973794438195,
                "origin_coord_y": 50.00136875782316,
                "destination_coord_x": 14.43109483523328,
                "destination_coord_y": 50.04052930943246,
                "datetime": "2018-05-28 09:03:40",
                "datasource": "funny_car",
            }
        }
