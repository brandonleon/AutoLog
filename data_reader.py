"""
This module contains the functions to query the database for logs and vehicles.
"""

import sqlite3
import typer
from rich.console import Console
from rich.table import Table
from constants import DB_FILE


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
            l.EntryType, l.Services
            FROM logs l
            LEFT JOIN vehicles v ON l.VehicleID = v.id
        """

        params = ()
        if vehicle_id:
            query += " WHERE l.VehicleID = ?"
            params = (vehicle_id,)

        query += " ORDER BY l.EntryDate DESC, l.EntryTime DESC LIMIT ? OFFSET ?"
        params += (page_size, (page - 1) * page_size)

        cursor.execute(query, params)
        if logs := cursor.fetchall():
            print(f"Page {page}:")
            console = Console()
            table = Table(
                "Vehicle", "EntryDate", "EntryTime", "EntryType", "Services"
            )
            for log in logs:

                table.add_row(f'{log[0]} {log[1]} {log[2]} {log[3]}', log[4], log[5], log[6], log[7])

            console.print(table)
            # Format the log data as needed

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
        query = "SELECT id, Make, Model, Year, mileage FROM vehicles"
        params = ()
        if vehicle_id:
            query += " WHERE id = ?"
            params = (vehicle_id,)

        query += " ORDER BY id LIMIT ? OFFSET ?"
        params += (page_size, (page - 1) * page_size)

        cursor.execute(query, params)
        if vehicles := cursor.fetchall():
            typer.echo(f"Page {page}:")
            for vehicle in vehicles:
                # Format the vehicle data as needed
                formatted_vehicle = (
                    f"id: {vehicle[0]}, Make: {vehicle[1]}, Model: {vehicle[2]}, "
                    f"Year: {vehicle[3]}, Miles: {vehicle[4]}"
                )
                typer.echo(formatted_vehicle)
        else:
            typer.echo("No vehicles found on this page.")
