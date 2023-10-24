import sqlite3
import typer
from constants import DB_FILE


def query_logs(page: int = 1, page_size: int = 10, vehicle_id: str = None):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        # Calculate the OFFSET based on the page number and page size
        offset = (page - 1) * page_size

        # Prepare the SQL query with parameterized query
        query = "SELECT EntryDate, EntryTime, EntryType, Services FROM logs"
        params = ()
        if vehicle_id:
            query += " WHERE VehicleID = ?"
            params = (vehicle_id,)

        query += " ORDER BY EntryDate, EntryTime LIMIT ? OFFSET ?"
        params += (page_size, (page - 1) * page_size)

        cursor.execute(query, params)
        if logs := cursor.fetchall():
            typer.echo(f"Page {page}:")
            for log in logs:
                # Format the log data as needed
                formatted_log = f"EntryDate: {log[0]}, EntryTime: {log[1]}, EntryType: {log[2]}"
                if Services := log[3]:
                    formatted_log += f", Services: {Services}"
                typer.echo(formatted_log)

        else:
            typer.echo("No logs found on this page.")


def query_vehicles(page: int = 1, page_size: int = 10, vehicle_id: str = None):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        # Calculate the OFFSET based on the page number and page size
        query = "SELECT id, Make, Model, Year FROM vehicles"
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
                formatted_vehicle = f"id: {vehicle[0]}, Make: {vehicle[1]}, Model: {vehicle[2]}, Year: {vehicle[3]}"
                typer.echo(formatted_vehicle)
        else:
            typer.echo("No vehicles found on this page.")