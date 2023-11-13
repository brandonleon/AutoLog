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


class FuelTypes(str, Enum):
    """
    Enum class representing different types of fuel.

    Explanation:
    This enum class defines various types of fuel that can be used in a vehicle.

    Attributes:
    - regular: Represents regular gasoline.
    - mid_grade: Represents mid-grade gasoline.
    - premium: Represents premium gasoline.
    - diesel: Represents diesel fuel.
    """

    regular = "Regular"
    mid_grade = "Mid-Grade"
    premium = "Premium"
    diesel = "Diesel"


@app.command()
def fuel_up(
    vehicle_id: Annotated[str, typer.Option(help="Vehicle ID")],
    odometer: Annotated[float, typer.Option(help="Odometer reading")],
    gallons: Annotated[float, typer.Option(help="Gallons filled")],
    cost_per_gallon: Annotated[float, typer.Option(help="Cost per gallon")],
    # Todo: Make default fuel type user configurable.
    fuel_type: Annotated[
        FuelTypes, typer.Option(help="Type of fuel")
    ] = FuelTypes.premium.value,
    entry_date: Annotated[
        str, typer.Option(help="Date of service")
    ] = datetime.now().strftime("%Y-%m-%d"),
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

    # convert Fuel type to the format used in the database:
    # "Regular" -> "Regular [Octane: 87]"
    # "Diesel" -> "Diesel [Centane: 40]"

    match fuel_type:
        case FuelTypes.regular:
            fuel_type = f"{fuel_type.value} [Octane: 87]"
        case FuelTypes.mid_grade:
            fuel_type = f"{fuel_type.value} [Octane: 89]"
        case FuelTypes.premium:
            fuel_type = f"{fuel_type.value} [Octane: 91]"
        case FuelTypes.diesel:
            fuel_type = f"{fuel_type.value} [Centane: 40]"
        case _:
            raise ValueError(f"Invalid fuel type: {fuel_type}")

    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        # Fetch the last fuel up entry for the vehicle to determine the MPG
        last_fuel_up_query = """
            SELECT OdometerReading, GallonsFilled
            FROM logs
            WHERE VehicleID = ? and EntryType = 'Gas'
            ORDER BY EntryDate DESC, EntryTime DESC
            LIMIT 1
            """
        cursor.execute(last_fuel_up_query, (vehicle_id,))
        if last_fuel_up := cursor.fetchone():
            last_odometer, last_gallons = last_fuel_up
            mpg = (
                (odometer - last_odometer) / last_gallons if last_gallons > 0 else None
            )
        else:
            mpg = None

        # Insert the fuel up entry
        query = """
            INSERT INTO logs (
                ID, VehicleID, EntryType, MPG, OdometerReading, 
                EntryDate, EntryTime, Location, CostPerGallon, 
                GallonsFilled, TotalCost, OctaneRating
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                str(uuid4()),
                vehicle_id,
                "Gas",
                mpg,
                odometer,
                entry_date,
                entry_time,
                location,
                f"${cost_per_gallon:.3f}",
                gallons,
                f"${cost_per_gallon * gallons:.2f}",
                fuel_type,
            ),
        ),

        query = "UPDATE vehicles SET mileage = ? WHERE id = ?"
        cursor.execute(query, (odometer, vehicle_id))
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
    ] = datetime.now().strftime("%Y-%m-%d"),
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
        query = "UPDATE vehicles SET mileage = ? WHERE id = ?"
        cursor.execute(query, (odometer, vehicle_id))
        conn.commit()
        typer.echo(f"Added log entry for {vehicle_id}.")


@app.command()
def vehicle(
    year: Annotated[int, typer.Option(help="Year of vehicle")],
    make: Annotated[str, typer.Option(help="Make of vehicle")],
    model: Annotated[str, typer.Option(help="Model of vehicle")],
    color: Annotated[str, typer.Option(help="Color of vehicle")],
    milage: Annotated[float, typer.Option(help="Odometer reading")],
    name: Annotated[str, typer.Option(help="Short name of vehicle")] = None,
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
                id, name, Year, Make, Model, mileage, trim, Engine, Color
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                str(uuid4()),
                name,
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
