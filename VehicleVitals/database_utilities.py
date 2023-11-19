"""
This module contains function to initialize the database and create the tables.
"""
import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv


def get_db_location() -> Path:
    """
    Check for the database configuration in the order of
    - .env file
    - Environment variable
    - Default value
    """
    # Check for .env file in the current directory
    env_file = Path(".") / ".env"
    if env_file.is_file():
        load_dotenv(dotenv_path=env_file)

        if database_url := os.getenv("VEHICLE_VITALS_DATABASE_LOCATION"):
            return Path.cwd() / database_url

    if database_url := os.getenv("VEHICLE_VITALS_DATABASE_LOCATION"):
        return Path(database_url)

    # If neither .env nor environment variable exists, use the default value as a Path object
    return Path.home() / ".config" / "VehicleVitals.db"


def initialize_database():
    sql_statements = Path(
        Path(__file__).parent.parent / "sql" / "init_database.sql"
    ).read_text()

    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()

        # Execute the SQL statements to create the tables
        cursor.executescript(sql_statements)
        conn.commit()


if __name__ == "__main__":
    initialize_database()
