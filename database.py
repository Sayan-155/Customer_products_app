"""
database.py
Small sqlite3 wrapper for the Motorcycle Compare app.
No ORM, no external DB server -- just a local .db file so the
whole project stays "run it and it works" with zero setup.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "motorcycles.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS motorcycles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    category TEXT NOT NULL,          -- Sport, Naked, Cruiser, Adventure, Touring, Scooter, Off-Road
    engine_cc INTEGER NOT NULL,
    cylinders INTEGER,
    power_hp REAL,
    torque_nm REAL,
    top_speed_kmh INTEGER,
    weight_kg INTEGER,
    seat_height_mm INTEGER,
    fuel_capacity_l REAL,
    mileage_kmpl REAL,
    transmission TEXT,
    abs TEXT,                         -- Yes / No / Optional
    price_usd INTEGER,
    image_emoji TEXT DEFAULT '🏍️'
);
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(reset=False):
    conn = get_connection()
    if reset:
        conn.execute("DROP TABLE IF EXISTS motorcycles")
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def is_empty():
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM motorcycles").fetchone()[0]
    conn.close()
    return count == 0
