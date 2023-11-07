"""
This module contains the functions to write from the database.
"""
import sqlite3
from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import uuid4

import typer

from .database_utilities import get_db_location
from .database_utilities import initialize_database

# Initialize the database (Create the file and tables if they don't exist).
initialize_database()
# Create the Typer app
app = typer.Typer()


class ServiceTypes(str, Enum):
    """
    Enum class representing different types of services.

    Explanation:
    This enum class defines various types of services that can be performed on a vehicle.

    Attributes:
    - air_filter: Represents an air filter service.
    - cabin_filter: Represents a cabin filter service.
    - oil_change: Represents an oil change service.
    - tire_rotation: Represents a tire rotation service.
    - tire_replacement: Represents a tire replacement service.
    - car_wash: Represents a car wash service.
    - car_detailing: Represents a car detailing service.
    """

    air_filter = "Air Filter"
    cabin_filter = "Cabin Filter"
    oil_change = "Oil Change"
    tire_rotation = "Tire Rotation"
    tire_replacement = "Tire Replacement"
    car_wash = "Car Wash"
    car_detailing = "Car Detailing"


@app.command()
def fuel_up(
    vehicle_id: Annotated[str, typer.Option(help="Vehicle ID")],
    odometer: Annotated[float, typer.Option(help="Odometer reading")],
    gallons: Annotated[float, typer.Option(help="Gallons filled")],
    cost_per_gallon: Annotated[float, typer.Option(help="Cost per gallon")],
    entry_date: Annotated[
        str, typer.Option(help="Date of service")
    ] = datetime.now().strftime("%m/%d/%Y"),
    entry_time: Annotated[
        str, typer.Option(help="Time of service")
    ] = datetime.now().strftime("%I:%M %p"),
    location: Annotated[str, typer.Option(help="Location of service")] = "Home",
):
    """
    Add a fuel up entry to the database.

    Example:
        vv add fuel-up --vehicle-id 23b3db142984 --odometer 1000 --gallons 10.0 --cost-per-gallon 2.50
    """
    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO logs (
                ID, VehicleID, EntryType, OdometerReading, 
                EntryDate, EntryTime, Location, CostPerGallon, 
                GallonsFilled, TotalCost
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                str(uuid4()),
                vehicle_id,
                "Gas",
                odometer,
                entry_date,
                entry_time,
                location,
                f"${cost_per_gallon:.3f}",
                gallons,
                f"${cost_per_gallon * gallons:.2f}",
            ),
        ),
        conn.commit()
        typer.echo(f"Added log entry for {vehicle_id}.")


@app.command()
def service(
    vehicle_id: Annotated[str, typer.Option(help="Vehicle ID")],
    odometer: Annotated[float, typer.Option(help="Odometer reading")],
    service_type: Annotated[ServiceTypes, typer.Option(help="Type of service")],
    cost: Annotated[float, typer.Option(help="Cost of service ($0.00)")],
    entry_date: Annotated[
        str, typer.Option(help="Date of service")
    ] = datetime.now().strftime("%m/%d/%Y"),
    entry_time: Annotated[
        str, typer.Option(help="Time of service")
    ] = datetime.now().strftime("%I:%M %p"),
    location: Annotated[str, typer.Option(help="Location of service")] = None,
):
    """
    Add a service entry to the database.

    Example:
        vv add service --vehicle-id 23b3db142984 --odometer 1000 --service-type "Oil Change" --cost 50.00
    """
    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO logs (
                ID, VehicleID, EntryType, OdometerReading, 
                EntryDate, EntryTime, Location, TotalCost, Services
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                str(uuid4()),
                vehicle_id,
                "Service",
                odometer,
                entry_date,
                entry_time,
                location,
                f"${cost:.2f}",
                service_type.value,
            ),
        ),
        # conn.commit()
        typer.echo(f"Added log entry for {vehicle_id}.")


def add_vehicle(year, make, model, trim, engine, color):
    pass


@app.command()
def vehicle(
    year: Annotated[int, typer.Option(help="Year of vehicle")],
    make: Annotated[str, typer.Option(help="Make of vehicle")],
    model: Annotated[str, typer.Option(help="Model of vehicle")],
    color: Annotated[str, typer.Option(help="Color of vehicle")],
    milage: Annotated[float, typer.Option(help="Odometer reading")],
    trim: Annotated[str, typer.Option(help="Trim level vehicle")] = None,
    engine: Annotated[str, typer.Option(help="Engine of vehicle")] = None,
):
    """
    Inserts a new vehicle record into the database.

    Example:
        vv add vehicle --year 2021 --make Honda --model Civic --mileage 1000 --color Red
    """

    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO vehicles (
                id, Year, Make, Model, mileage, trim, Engine, Color
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                str(uuid4()),
                year,
                make,
                model,
                milage,
                trim,
                engine,
                color,
            ),
        ),
        conn.commit()
        typer.echo(f"Added vehicle {year} {make} {model}, to the database.")


if __name__ == "__main__":
    app()
