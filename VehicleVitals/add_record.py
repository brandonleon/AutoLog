"""
This module contains the functions to write from the database.
"""
import sqlite3
from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import uuid4

import typer

from .constants import DB_FILE
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


def add_service(
    vehicle_id: str,
    odometer: float,
    entry_date: str,
    entry_time: str,
    location: str,
    service_type: ServiceTypes,
    cost: float,
):
    """
    Adds a service log entry for a vehicle.

    Args:
        vehicle_id (str): The ID of the vehicle.
        odometer (float): The odometer reading at the time of the service.
        entry_date (str): The date of the service entry (default: today's date).
        entry_time (str): The time of the service entry (default: current time).
        location (str): The location of the service.
        service_type (ServiceTypes): The type of service performed.
        cost (float): The cost of the service.

    Returns:
        None

    Examples:
        add_service(
            vehicle_id="ABC123",
            odometer=10000.0,
            entry_date="2022-01-01",
            entry_time="09:00:00",
            location="Home",
            service_type=ServiceTypes.oil_change,
            cost=50.0,
        )
    """

    with sqlite3.connect(DB_FILE) as conn:
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
                service_type.value
            ),
        ),
        # conn.commit()
        typer.echo(f"Added log entry for {vehicle_id}.")


def add_fuel_up(
    vehicle_id: str,
    odometer: float,
    entry_date: str,
    entry_time: str,
    location: str,
    cost_per_gallon: float,
    gallons: float,
):
    """
    Adds a fuel-up log entry for a vehicle.

    Args:
        vehicle_id (str): The ID of the vehicle.
        odometer (float): The odometer reading at the time of the fuel-up.
        entry_date (str): The date of the fuel-up entry (default: today's date).
        entry_time (str): The time of the fuel-up entry (default: current time).
        location (str): The location of the fuel-up.
        cost_per_gallon (float): The cost per gallon of fuel
        gallons (float): The number of gallons filled.

    Returns:
        None

    Examples:
        add_fuel_up(
            vehicle_id="ABC123",
            odometer=10000.0,
            entry_date="2022-01-01",
            entry_time="09:00:00",
            location="Shell",
            cost_per_gallon=2.5,
            gallons=10.0,
        )
    """

    with sqlite3.connect(DB_FILE) as conn:
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
    """
    add_service(
        vehicle_id,
        odometer,
        entry_date,
        entry_time,
        location,
        service_type,
        cost,
    )


if __name__ == "__main__":
    app()
