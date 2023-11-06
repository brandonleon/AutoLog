"""
This module contains the functions to write from the database.
"""
import sqlite3
from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import uuid4

import typer
from icecream import ic

from constants import DB_FILE
from database_utilities import initialize_database

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
    - gas: Represents a gas service.
    - air_filter: Represents an air filter service.
    - cabin_filter: Represents a cabin filter service.
    - oil_change: Represents an oil change service.
    - tire_rotation: Represents a tire rotation service.
    - tire_replacement: Represents a tire replacement service.
    - car_wash: Represents a car wash service.
    - car_detailing: Represents a car detailing service.
    """

    gas = "Gas"
    air_filter = "Air Filter"
    cabin_filter = "Cabin Filter"
    oil_change = "Oil Change"
    tire_rotation = "Tire Rotation"
    tire_replacement = "Tire Replacement"
    car_wash = "Car Wash"
    car_detailing = "Car Detailing"


def add_service():
    pass


def add_fuel_up(
    vehicle_id: str,
    odometer: float,
    entry_date: str,
    entry_time: str,
    location: str,
    cost_per_gallon: float,
    gallons: float,
):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO logs (
                ID, VehicleID, EntryType, OdometerReading, 
                EntryDate, EntryTime, Location, CostPerGallon, 
                GallonsFilled, TotalCost
            ) 
            VALUES (?, ?, "Gas", ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                str(uuid4()),
                vehicle_id,
                odometer,
                entry_date,
                entry_time,
                location,
                f"${cost_per_gallon:.3f}",
                gallons,
                f"${cost_per_gallon * gallons:.2f}",
            )),
        conn.commit()
        typer.echo(f"Added log entry for {vehicle_id}.")


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
    """
    add_fuel_up(
        vehicle_id,
        odometer,
        entry_date,
        entry_time,
        location,
        cost_per_gallon,
        gallons,
    )


@app.command()
def service():
    pass


if __name__ == "__main__":
    app()
