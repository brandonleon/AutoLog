"""
This module contains the functions to write from the database.
"""

import sqlite3
import typer
from rich.console import Console
from rich.table import Table
from constants import DB_FILE
from uuid import uuid4


def add_record(vehicle_id: str,
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
        match Services:
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

        cursor.execute(query, (str(uuid4()), vehicle_id, odometer, entry_date, entry_time, entry location, total_cost, service))
        conn.commit()
        typer.echo(f"Added log entry for {vehicle_id}.")
