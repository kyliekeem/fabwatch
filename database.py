
import sqlite3


def initialize_database():
    connection = sqlite3.connect("fabwatch.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id TEXT NOT NULL,
            pressure REAL NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_reading(equipment_id, pressure, status):
    connection = sqlite3.connect("fabwatch.db")

    connection.execute("""
        INSERT INTO sensor_readings
        (equipment_id, pressure, status)
        VALUES (?, ?, ?)
    """, (equipment_id, pressure, status))

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("FabWatch database initialized successfully!")
