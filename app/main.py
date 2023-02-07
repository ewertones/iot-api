"""
This module is the main script of a FastAPI application that provides APIs to collect IoT trip data.

It sets up the FastAPI app, creates database tables, and defines routes and functions.
It provides functionality for creating a trip, retrieving multiple trips, and bulk creating them.
"""
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html

from sqlalchemy.orm import Session

from crud.trips import (
    get_trips as crud_get_trips,
    create_trip as crud_create_trip,
    create_trips as crud_create_trips,
)
from database.database import SessionLocal, db_engine
from schemas.schemas import TripCreate, TripGet, OKMessage
from models.models import Base


# Initialize the FastAPI app
app = FastAPI(
    title="IoT API",
    description="A simple API to collect IoT trip data.",
    version="0.0.1",
    contact={
        "name": "Ewerton Souza",
        "email": "ewerton@ewerton.com.br",
    },
)

# Create/Update tables in the database
Base.metadata.create_all(bind=db_engine)

# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Customize the OpenAPI schema for the FastAPI app
def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get("paths").items():
            for _, param in method_item.items():
                responses = param.get("responses")
                if "422" in responses:
                    del responses["422"]
                if ("200" in responses) and ("post" in param.get("operationId")):
                    del responses["200"]

    return app.openapi_schema


# Set the custom OpenAPI schema for the FastAPI app
app.openapi = custom_openapi


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse("favicon.ico")


@app.get("/", include_in_schema=False)
@app.get("/docs", include_in_schema=False)
async def docs():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        swagger_favicon_url="favicon.ico",
        title="IoT API - Ewerton Souza",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    )


@app.post(
    "/trip",
    tags=["User"],
    status_code=201,
    responses={201: {"model": OKMessage, "description": "Created"}},
)
def create_trip(trip: TripCreate, db: Session = Depends(get_db)) -> str:
    crud_create_trip(trip, db)
    return "OK"


@app.get("/trips", tags=["User"], response_model=list[TripGet])
def get_trips(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> list[TripGet]:
    trips = crud_get_trips(skip, limit, db)
    return trips


@app.post(
    "/trips",
    tags=["User"],
    status_code=201,
    responses={201: {"model": OKMessage, "description": "Created"}},
)
def create_trips(trips: list[TripCreate], db: Session = Depends(get_db)) -> str:
    crud_create_trips(trips, db)
    return "OK"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080)
