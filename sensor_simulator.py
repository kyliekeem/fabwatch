import random
import csv

# Equipment settings
EQUIPMENT_ID = "ETCH-001"
SETPOINT = 50.0
LOWER_LIMIT = 45.0
UPPER_LIMIT = 55.0

# Create CSV file
with open("sensor_data.csv", "w", newline="") as file:
    writer = csv.writer(file)

    # Write column names
    writer.writerow([
        "second",
        "equipment_id",
        "pressure_mTorr",
        "status"
    ])

    # Generate sensor readings
    for second in range(10):
        pressure = round(random.gauss(SETPOINT, 1.5), 2)

        # Inject anomaly
        if second == 7:
            pressure = 65.0

        # Anomaly detection
        if pressure < LOWER_LIMIT or pressure > UPPER_LIMIT:
            status = "WARNING"
        else:
            status = "NORMAL"

        # Display result
        print(f"{second:02d}s | {pressure:.2f} mTorr | {status}")

        # Save result
        writer.writerow([
            second,
            EQUIPMENT_ID,
            pressure,
            status
        ])

print("\nSensor data saved to sensor_data.csv")
