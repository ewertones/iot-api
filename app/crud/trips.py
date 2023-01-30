"""File contains the CRUD operations for the trips data."""
from sqlalchemy.orm import Session
from models.models import TripsTable
from schemas.schemas import TripCreate, TripGet


class Point:
    """The `Point` class is used to parse coordinates from IoT devices"""

    def __init__(self, x):
        self.x, self.y = map(
            float, x.replace("POINT (", "").replace(")", "").split(" ")
        )


# Returns a list of trip objects, filtered by skip and limit, from the database
def get_trips(skip: int, limit: int, db: Session) -> list[TripGet]:
    # Retrieve trips data from the database
    trips = (
        db.query(TripsTable)
        .with_entities(
            TripsTable.region,
            TripsTable.origin_coord_x,
            TripsTable.origin_coord_y,
            TripsTable.destination_coord_x,
            TripsTable.destination_coord_y,
            TripsTable.datetime,
            TripsTable.datasource,
        )
        .order_by(TripsTable.datetime)
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Convert the data into the desired format (TripGet)
    parsed_trips = [
        TripGet(
            region=region,
            origin_coord_x=origin_coord_x,
            origin_coord_y=origin_coord_y,
            destination_coord_x=destination_coord_x,
            destination_coord_y=destination_coord_y,
            datetime=datetime.strftime("%Y-%m-%d %H:%M:%S"),
            datasource=datasource,
        )
        for region, origin_coord_x, origin_coord_y, destination_coord_x, destination_coord_y, datetime, datasource in trips
    ]

    return parsed_trips


# Converts the trip object from the input format (TripCreate) to the database format (TripsTable)
def parse_trip(trip: TripCreate) -> TripsTable:
    origin_coord = Point(trip.origin_coord)
    destination_coord = Point(trip.destination_coord)
    db_trip = TripsTable(
        region=trip.region,
        origin_coord_x=origin_coord.x,
        origin_coord_y=origin_coord.y,
        destination_coord_x=destination_coord.x,
        destination_coord_y=destination_coord.y,
        datetime=trip.datetime,
        datasource=trip.datasource,
    )
    return db_trip


# Add a single trip to the database
def create_trip(trip: TripCreate, db: Session) -> None:
    # Convert the trip object to the database format
    db_trip = parse_trip(trip)

    # Add the trip object to the database
    db.add(db_trip)

    # commit all changes to the database
    db.commit()


# Add multiple trips to the database at once.
def create_trips(trips: list[TripCreate], db: Session) -> None:
    for trip in trips:
        db_trip = parse_trip(trip)
        db.add(db_trip)

    # commit all changes to the database
    db.commit()
