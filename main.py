"""
This is the main entry point for the application. It creates the Typer app and
defines the commands that can be run from the command line.
"""
from datetime import datetime
from typing import Annotated
from enum import Enum

import typer
from data_reader import query_logs, query_vehicles
# from data_writer import add_record TODO: complete logic in data_writer.py
from database_utilities import initialize_database

# Initialize the database (Create the file and tables if they don't exist).
initialize_database()
# Create the Typer app
app = typer.Typer()


@app.command()
def display_logs(
        page: Annotated[int, typer.Option(help="Page number to retrieve.")] = 1,
        page_size: Annotated[int, typer.Option(help="Number of records per page.")] = 10,
        vehicle_id: Annotated[
            str, typer.Option(help="Filter by Vehicle ID (All if blank).")
        ] = "",
):
    """
    View logs with optional filtering and pagination.

    page: The page number to display.
    page_size: The number of records to display per page.
    vehicle_id: The vehicle ID to filter on.
    """
    query_logs(page, page_size, vehicle_id)


@app.command()
def display_vehicles(
        page: Annotated[int, typer.Option(help="Page number to retrieve.")] = 1,
        page_size: Annotated[int, typer.Option(help="Number of records per page.")] = 10,
        vehicle_id: Annotated[
            str, typer.Option(help="Filter by Vehicle ID (All if blank).")
        ] = "",
):
    """
    View vehicles with optional filtering and pagination.

    page: The page number to display.
    page_size: The number of records to display per page.
    vehicle_id: The vehicle ID to filter on.
    """
    query_vehicles(page, page_size, vehicle_id)


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
        entry_date: Annotated[str, typer.Option(help="Date of service")] = datetime.now().strftime("%m/%d/%Y"),
        entry_time: Annotated[str, typer.Option(help="Time of service")] = datetime.now().strftime("%I:%M %p"),
        location: Annotated[str, typer.Option(help="Location of service")] = "Home",
        total_cost: Annotated[float, typer.Option(help="Total cost of service")] = '$0.0'
):
    """
    Add a log entry for a vehicle.
    TODO: complet logic in data_writer.py
    """
    pass


if __name__ == "__main__":
    app()
