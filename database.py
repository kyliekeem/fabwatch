import sqlite3

# Connect to database
connection = sqlite3.connect("fabwatch.db")

# Create sensor readings table
connection.execute("""
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipment_id TEXT NOT NULL,
        pressure REAL NOT NULL,
        status TEXT NOT NULL,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")

# Save changes
connection.commit()
connection.close()

print("FabWatch database initialized successfully!")

def save_reading(equipment_id, pressure, status):
    connection = sqlite3.connect("fabwatch.db")

    connection.execute("""
        INSERT INTO sensor_readings
        (equipment_id, pressure, status)
        VALUES (?, ?, ?)
    """, (equipment_id, pressure, status))

    connection.commit()
    connection.close()
