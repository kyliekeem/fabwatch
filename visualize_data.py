import csv
import matplotlib.pyplot as plt

# Store CSV data
seconds = []
pressures = []
statuses = []

# Read sensor data
with open("sensor_data.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        seconds.append(int(row["second"]))
        pressures.append(float(row["pressure_mTorr"]))
        statuses.append(row["status"])

# Draw pressure line
plt.plot(seconds, pressures, marker="o", label="Pressure")

# Draw acceptable limits
plt.axhline(y=55, linestyle="--", color="red", label="Upper Limit")
plt.axhline(y=45, linestyle="--", color="orange", label="Lower Limit")

# Highlight anomalies
for second, pressure, status in zip(seconds, pressures, statuses):
    if status == "WARNING":
        plt.scatter(second, pressure, color="red", s=100, zorder=5)

# Chart labels
plt.title("FabWatch - ETCH-001 Pressure Monitoring")
plt.xlabel("Simulated Time (seconds)")
plt.ylabel("Chamber Pressure (mTorr)")
plt.legend()
plt.grid(True)

# Save and display
plt.savefig("pressure_chart.png", dpi=150, bbox_inches="tight")
plt.show()
