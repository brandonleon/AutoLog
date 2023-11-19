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
    "part_id"       TEXT,
    PRIMARY KEY("id"),
    FOREIGN KEY ("part_id") REFERENCES "parts" ("id")
);
