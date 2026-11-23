import sqlite3

from database import initialize_database, save_reading


def test_save_reading(tmp_path, monkeypatch):
    # Use an isolated temporary directory
    monkeypatch.chdir(tmp_path)

    # Initialize test database
    initialize_database()

    # Save a simulated sensor reading
    save_reading("ETCH-001", 65.0, "WARNING")

    # Read data from the database
    connection = sqlite3.connect("fabwatch.db")

    result = connection.execute("""
        SELECT equipment_id, pressure, status
        FROM sensor_readings
    """).fetchone()

    connection.close()

    # Verify saved data
    assert result == ("ETCH-001", 65.0, "WARNING")
