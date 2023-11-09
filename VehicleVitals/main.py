"""
This is the main entry point for the application. It creates the Typer app and
defines the commands that can be run from the command line.
"""
import typer

from . import add_record
from . import display
from .database_utilities import initialize_database

# Initialize the database (Create the file and tables if they don't exist).
initialize_database()

app = typer.Typer()
app.add_typer(display.app, name="display", help="Display records from the database.")
app.add_typer(add_record.app, name="add", help="Add records to the database.")


if __name__ == "__main__":
    app()
