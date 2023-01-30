"""
This module defines the TripsTable model which represents the trips data
stored in a relational database using SQLAlchemy. It includes columns for
region, origin coordinates, destination coordinates, date, datasource,
created and updated timestamps.
"""
from sqlalchemy import Column, Float, String, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TripsTable(Base):
    """SQLAlchemy ORM model for the trips table."""

    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    region = Column(String, nullable=False)
    origin_coord_x = Column(Float, nullable=False)
    origin_coord_y = Column(Float, nullable=False)
    destination_coord_x = Column(Float, nullable=False)
    destination_coord_y = Column(Float, nullable=False)
    datetime = Column(DateTime, nullable=False)
    datasource = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
