"""
This module contains function to initialize the database and create the tables.
"""

import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

INIT_DATABASE_SQL = """
-- logs table
CREATE TABLE IF NOT EXISTS "logs" (
    ID              TEXT,
    VehicleID       TEXT
        CONSTRAINT logs_vehicles_id_fk REFERENCES vehicles,
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
);

-- vehicles table
CREATE TABLE IF NOT EXISTS "vehicles" (
    "id"        TEXT NOT NULL,
    "name"      TEXT,
    "Year"      INTEGER NOT NULL,
    "Make"      TEXT NOT NULL,
    "Model"     TEXT NOT NULL,
    "trim"      TEXT,
    "Engine"    TEXT,
    "Color"     TEXT NOT NULL,
    "mileage"   REAL NOT NULL DEFAULT 0,
    PRIMARY KEY("id")
);

-- parts table
CREATE TABLE IF NOT EXISTS "parts" (
    "id"            TEXT NOT NULL,
    "name"          TEXT,
    "description"   TEXT,
    "cost"          REAL,
    PRIMARY KEY("id")
);

-- service_types table
CREATE TABLE IF NOT EXISTS "service_types" (
    "id"            TEXT NOT NULL,
    "name"          TEXT,
    "description"   TEXT,
    "interval_days" INTEGER,
    "interval_miles" INTEGER,
    PRIMARY KEY("id")
);

-- service_type_parts table (junction table)
CREATE TABLE IF NOT EXISTS "service_type_parts" (
    "service_type_id" TEXT NOT NULL,
    "part_id"         TEXT NOT NULL,
    PRIMARY KEY("service_type_id", "part_id"),
    FOREIGN KEY ("service_type_id") REFERENCES "service_types" ("id"),
    FOREIGN KEY ("part_id") REFERENCES "parts" ("id")
);
"""


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

    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()

        # Execute the SQL statements to create the tables
        cursor.executescript(INIT_DATABASE_SQL)
        conn.commit()


if __name__ == "__main__":
    initialize_database()
