"""
This module contains the functions to read from the database.
"""
import sqlite3
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from .constants import DB_FILE
from .database_utilities import initialize_database

# Initialize the database (Create the file and tables if they don't exist).
initialize_database()
# Create the Typer app
app = typer.Typer()


def query_logs(page: int = 1, page_size: int = 10, vehicle_id: str = None):
    """
    Query the logs table and display the results.

    page: The page number to display.
    page_size: The number of records to display per page.
    vehicle_id: The vehicle ID to filter on.
    """
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        # Calculate the OFFSET based on the page number and page size
        offset = (page - 1) * page_size

        # Prepare the SQL query with parameterized query
        query = """
            SELECT v.Year, v.Make, v.Model, v.trim, l.EntryDate, l.EntryTime,
            l.OdometerReading, l.EntryType, l.Services
            FROM logs l
            LEFT JOIN vehicles v ON l.VehicleID = v.id
        """

        params = ()
        if vehicle_id:
            query += " WHERE l.VehicleID = ?"
            params = (vehicle_id,)

        query += " ORDER BY l.EntryDate DESC, l.EntryTime DESC LIMIT ? OFFSET ?"
        params += (page_size, offset)

        cursor.execute(query, params)
        if log_entries := cursor.fetchall():
            print(f"Page {page}:")
            console = Console()
            table = Table(
                "Vehicle", "EntryDate", "EntryTime", "Odometer", "EntryType", "Services"
            )
            for log in log_entries:
                table.add_row(
                    f"{log[0]} {log[1]} {log[2]} {log[3]}",
                    log[4],
                    log[5],
                    f"{float(str(log[6]).replace(',', '')):,.1f}",
                    log[7],
                    log[8],
                )
            console.print(table)
        else:
            typer.echo("No logs found on this page.")


def query_vehicles(page: int = 1, page_size: int = 10, vehicle_id: str = None):
    """
    Query the vehicles table and display the results.

    page: The page number to display.
    page_size: The number of records to display per page.
    vehicle_id: The vehicle ID to filter on.
    """
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        # Calculate the OFFSET based on the page number and page size
        query = "SELECT id, Year, Make, Model, Year, mileage FROM vehicles"
        params = ()
        if vehicle_id:
            query += " WHERE id = ?"
            params = (vehicle_id,)

        query += " ORDER BY id LIMIT ? OFFSET ?"
        params += (page_size, (page - 1) * page_size)

        cursor.execute(query, params)
        if vehicle_entries := cursor.fetchall():
            print(f"Page {page}:")
            console = Console()
            table = Table("id", "year", "make", "Model", "trim", "mileage")
            for vehicle in vehicle_entries:
                v = [str(x) for x in vehicle]
                table.add_row(*v)

            console.print(table)
        else:
            typer.echo("No vehicles found on this page.")


@app.command()
def logs(
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
def vehicles(
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
