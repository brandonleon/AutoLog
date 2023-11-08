"""
This module contains the functions to read from the database.
"""
import sqlite3
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from .database_utilities import get_db_location
from .database_utilities import initialize_database


# Initialize the database (Create the file and tables if they don't exist).
initialize_database()
# Create the Typer app
app = typer.Typer()


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

    Examples:

        vv display logs


        vv display logs --vehicle-id 6a9ab94e-0cea-481d-a9d4-23b3db142984
    """
    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()

        # Calculate the OFFSET based on the page number and page size
        offset = (page - 1) * page_size

        # Prepare the SQL query with parameterized query
        query = """
            SELECT v.Year, v.Make, v.Model, v.trim, l.EntryDate, l.EntryTime,
            l.OdometerReading, l.MPG, l.EntryType, l.Services
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
                "Vehicle", "EntryDate", "EntryTime", "Odometer", "MPG", "EntryType", "Services"
            )
            for log in log_entries:
                table.add_row(
                    f"{log[0]} {log[1]} {log[2]} {log[3]}",
                    log[4],
                    log[5],
                    f"{float(log[6]):,.1f}" if log[6] is not None else "N/A",
                    f"{float(log[7]):,.1f}" if log[7] is not None else "N/A",
                    log[8],
                    log[9],
                )
            console.print(table)
        else:
            typer.echo("No logs found on this page.")


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

    Examples:

        vv display vehicles


        vv display vehicles --vehicle-id 6a9ab94e-0cea-481d-a9d4-23b3db142984
    """
    with sqlite3.connect(get_db_location()) as conn:
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
                table.add_row(
                    v[0],
                    v[1],
                    v[2],
                    v[3],
                    v[4],
                    f"{float(str(v[5]).replace(',', '')):,.1f}",
                )

            console.print(table)
        else:
            typer.echo("No vehicles found on this page.")


if __name__ == "__main__":
    app()
