import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "patients.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT,
            diagnosis TEXT
        )
        """
    )
    conn.execute(
        """
        INSERT INTO patients (name, age, gender, phone, diagnosis)
        SELECT 'John Doe', 45, 'male', '555-0100', 'Hypertension'
        WHERE NOT EXISTS (SELECT 1 FROM patients)
        """
    )
    conn.commit()
    conn.close()
