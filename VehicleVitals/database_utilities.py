"""
This module contains function to initialize the database and create the tables.
"""
import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv


def get_db_location() -> Path:
    """
    Check for the database configuration in the order of:
    1. Look for a .env file in the current directory and load its content.
    2. Check for the environment variable VEHICLE_VITALS_DATABASE_LOCATION.
    3. Use the default value if neither .env nor environment variable exists.

    Returns:
        Path: Path object representing the location of the database.
    """
    # 1. Check for .env file in the current directory
    env_file = Path(".") / ".env"
    if env_file.is_file():
        load_dotenv(dotenv_path=env_file)

    # 2. Check for environment variable
    if database_url := os.getenv("VEHICLE_VITALS_DATABASE_LOCATION"):
        return Path(database_url)

    # 3. Use the default value
    return Path.home() / ".config" / "VehicleVitals.db"


def initialize_database():
    """
    Load the SQL statements from the init_database.sql file and execute them.
    If database or tables do not exist, they will be created.
    Returns:
        None
    """
    sql_statements = Path(
        Path(__file__).parent / "sql" / "init_database.sql"
    ).read_text()

    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()

        # Execute the SQL statements to create the tables
        cursor.executescript(sql_statements)
        conn.commit()


if __name__ == "__main__":
    initialize_database()
