"""
This module contains function to initialize the database and create the tables.
"""

import sqlite3
from constants import DB_FILE


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
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        # Execute the SQL statements to create the tables
        cursor.execute(create_logs_table_sql)
        cursor.execute(create_vehicles_table_sql)
