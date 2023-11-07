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
    create_logs_table_sql = """
CREATE TABLE IF NOT EXISTS "logs"
(
    ID              TEXT,
    VehicleID       TEXT
        constraint logs_vehicles_id_fk
            references vehicles,
    EntryType       TEXT,
    MPG             REAL,
    EntryDate       TEXT,
    EntryTime       TEXT,
    OdometerReading REAL,
    IsFillUp        TEXT,
    CostPerGallon   REAL,
    GallonsFilled   REAL,
    TotalCost       REAL,
    OctaneRating    INT,
    GasBrand        TEXT,
    Location        TEXT,
    EntryTags       TEXT,
    PaymentType     TEXT,
    TirePressure    TEXT,
    Notes           TEXT,
    Services        TEXT
)
"""
    create_vehicles_table_sql = """
CREATE TABLE IF NOT EXISTS "vehicles" (
    "id"        TEXT NOT NULL,
    "Year"      INTEGER NOT NULL,
    "Make"      TEXT NOT NULL,
    "Model"     TEXT NOT NULL,
    "trim"      text,
    "Engine"    TEXT,
    "Color"     TEXT NOT NULL,
    "mileage"   real NOT NULL DEFAULT 0,
    PRIMARY KEY("id")
)
"""
    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()

        # Execute the SQL statements to create the tables
        cursor.execute(create_logs_table_sql)
        cursor.execute(create_vehicles_table_sql)
