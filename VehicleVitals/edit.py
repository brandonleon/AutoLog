"""
This module contains the functions to edit entries in the database.
"""
import sqlite3
from typing import Annotated

import typer

from .database_utilities import get_db_location

# Create the Typer app
app = typer.Typer()


@app.command()
def vehicle(
    vehicle: Annotated[str, typer.Option(help="ID or Name of the vehicle")] = None,
    year: Annotated[int, typer.Option(help="Year of vehicle")] = None,
    make: Annotated[str, typer.Option(help="Make of vehicle")] = None,
    model: Annotated[str, typer.Option(help="Model of vehicle")] = None,
    color: Annotated[str, typer.Option(help="Color of vehicle")] = None,
    mileage: Annotated[float, typer.Option(help="Odometer reading")] = None,
    name: Annotated[str, typer.Option(help="Short name of vehicle")] = None,
    trim: Annotated[str, typer.Option(help="Trim level vehicle")] = None,
    engine: Annotated[str, typer.Option(help="Engine of vehicle")] = None,
):
    """
    Edit a vehicle record in the database, based on the vehicle ID or name.
    Only values that are passed in will be updated.
    Args:
        vehicle: ID or Name of the vehicle
        year:
        make:
        model:
        color:
        mileage:
        name:
        trim:
        engine:
    """
    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()

        set_clause = [
            f"{field} = ?"
            for field, value in [
                ("year", year),
                ("make", make),
                ("model", model),
                ("color", color),
                ("mileage", mileage),
                ("name", name),
                ("trim", trim),
                ("engine", engine),
            ]
            if value is not None
        ]
        # Join the SET clause into a comma-separated string
        set_clause = ", ".join(set_clause)

        # Prepare the SQL query with parameterized query
        query = f"UPDATE vehicles SET {set_clause} WHERE id = ? or name = ?"

        params = [
            field
            for field in [
                year,
                make,
                model,
                color,
                mileage,
                name,
                trim,
                engine,
            ]
            if field
        ]

        params += [vehicle, vehicle]

        cursor.execute(query, params)
        conn.commit()
        typer.echo(f"Updated vehicle {vehicle}.")


if __name__ == "__main__":
    app()
