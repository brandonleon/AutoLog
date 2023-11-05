"""
This is the main entry point for the application. It creates the Typer app and
defines the commands that can be run from the command line.
"""
from datetime import datetime
from typing import Annotated
from enum import Enum

import typer
import display
from data_writer import add_record
from database_utilities import initialize_database

# Initialize the database (Create the file and tables if they don't exist).
initialize_database()
# Create the Typer app
app = typer.Typer()
app.add_typer(display.app, name="display")


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
def add_log_entry(
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
    Add a log entry for a vehicle.
    """
    add_record(
        vehicle_id, odometer, service, entry_date, entry_time, location, total_cost
    )


if __name__ == "__main__":
    app()
