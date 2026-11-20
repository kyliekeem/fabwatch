import sqlite3

# Connect to database
connection = sqlite3.connect("fabwatch.db")

# Count all readings
total = connection.execute(
    "SELECT COUNT(*) FROM sensor_readings"
).fetchone()[0]

# Find abnormal readings
anomalies = connection.execute("""
    SELECT id, equipment_id, pressure, timestamp
    FROM sensor_readings
    WHERE status = 'WARNING'
    ORDER BY id DESC
""").fetchall()

# Calculate anomaly rate
anomaly_count = len(anomalies)

if total > 0:
    anomaly_rate = (anomaly_count / total) * 100
else:
    anomaly_rate = 0.0

print("=== FabWatch Historical Analysis ===")
print(f"Total readings: {total}")
print(f"Anomalies detected: {anomaly_count}")
print(f"Anomaly rate: {anomaly_rate:.2f}%")

# Display anomaly history
print("\n=== Anomaly History ===")

for record in anomalies:
    print(record)

connection.close()
