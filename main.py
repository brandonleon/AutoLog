"""
This is the main entry point for the application. It creates the Typer app and
defines the commands that can be run from the command line.
"""
from typing import Annotated

import typer
from query import query_logs, query_vehicles
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


if __name__ == "__main__":
    app()
