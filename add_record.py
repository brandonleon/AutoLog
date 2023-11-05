"""
This module contains the functions to write from the database.
"""
import sqlite3
from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import uuid4

import typer

from constants import DB_FILE
from database_utilities import initialize_database

# Initialize the database (Create the file and tables if they don't exist).
initialize_database()
# Create the Typer app
app = typer.Typer()


def add_fuel_up(
    vehicle_id: str,
    odometer: float,
    service: str,
    entry_date: str,
    entry_time: str,
    location: str,
    total_cost: float,
):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO logs (ID, VehicleID, OdometerReading, EntryDate, EntryTime, Location, TotalCost, Services)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        match service:
            case "Gas":
                EntryType = "Gas"
            case "Air Filter":
                EntryType = "Maintenance"
                Services = "Air Filter"
            case "Cabin Filter":
                EntryType = "Maintenance"
                Services = "Cabin Filter"
            case "Oil Change":
                EntryType = "Maintenance"
                Services = "Oil Change"
            case "Tire Rotation":
                EntryType = "Maintenance"
                Services = "Tire Rotation"
            case "Tire Replacement":
                EntryType = "Maintenance"
                Services = "Tire Replacement"
            case "Car Wash":
                EntryType = "Wash"
                Services = "Car Wash"
            case "Car Detailing":
                EntryType = "Wash"
                Services = "Car Detailing"
            case _:
                EntryType = "Other"

        cursor.execute(
            query,
            (
                str(uuid4()),
                vehicle_id,
                odometer,
                entry_date,
                entry_time,
                location,
                total_cost,
                service,
            ),
        )
        conn.commit()
        typer.echo(f"Added log entry for {vehicle_id}.")


class ServiceTypes(str, Enum):
    gas = "Gas"
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
    service: Annotated[ServiceTypes, typer.Option(help="Service performed")],
    entry_date: Annotated[
        str, typer.Option(help="Date of service")
    ] = datetime.now().strftime("%m/%d/%Y"),
    entry_time: Annotated[
        str, typer.Option(help="Time of service")
    ] = datetime.now().strftime("%I:%M %p"),
    location: Annotated[str, typer.Option(help="Location of service")] = "Home",
    total_cost: Annotated[float, typer.Option(help="Total cost of service")] = "0.0",
):
    """
    Add a fuel up entry to the database.
    """
    add_fuel_up(
        vehicle_id, odometer, service, entry_date, entry_time, location, total_cost
    )


if __name__ == "__main__":
    app()
