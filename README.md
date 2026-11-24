
# FabWatch
### Semiconductor Equipment Monitoring & Anomaly Detection Simulator

[![FabWatch CI](https://github.com/kyliekeem/fabwatch/actions/workflows/tests.yml/badge.svg)](https://github.com/kyliekeem/fabwatch/actions/workflows/tests.yml)

FabWatch is a Python-based monitoring application that simulates semiconductor etching equipment, detects abnormal chamber pressure readings, and visualizes equipment performance through an interactive dashboard.

The project demonstrates data generation, threshold-based anomaly detection, persistent storage, historical analytics, and automated testing.

> **Note:** FabWatch uses simulated sensor data and educational process thresholds. It is not connected to real semiconductor manufacturing equipment.

## Features

- **Sensor Simulation:** Generates synthetic chamber pressure readings using a Gaussian distribution.
- **Anomaly Detection:** Detects pressure readings outside configurable thresholds.
- **Live Monitoring:** Updates equipment metrics and charts approximately every second.
- **SQLite Storage:** Persists sensor readings across application restarts.
- **Historical Analytics:** Calculates anomaly counts and anomaly rates using SQL queries.
- **Automated Testing:** Validates anomaly detection logic with Pytest.
- **Fault Injection:** Simulates high-pressure, low-pressure, and invalid sensor readings.
- **Simulation Controls:** Supports Pause, Resume, and Reset operations.
- **Sensor Validation:** Rejects NaN and infinite sensor readings.
- **CSV Export:** Exports historical anomaly records for further analysis.
- **Automated Testing:** Includes 12 unit and integration tests.
- **CI Pipeline:** Runs automated tests through GitHub Actions.

## Dashboard Preview

![FabWatch Monitoring Dashboard](docs/fabwatch-dashboard.png)

## Tech Stack

- Python
- Streamlit
- Pandas
- SQLite
- Matplotlib
- Pytest
- Git & GitHub

## System Architecture

```text
Simulated Etching Equipment
            |
            v
   Pressure Data Generator
            |
            v
   Anomaly Detection Logic
            |
      +-----+-----+
      |           |
      v           v
Session State   SQLite
      |           |
      v           v
Live Monitoring  Historical Analytics
      |           |
      +-----+-----+
            |
            v
    Streamlit Dashboard
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/kyliekeem/fabwatch.git
cd fabwatch
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Initialize the database

```bash
python database.py
```

### 5. Run the live dashboard

```bash
python -m streamlit run live_dashboard.py
```

Open the local URL displayed in the terminal.

## Running Tests

```bash
python -m pytest -v
```

The current unit test suite covers:

- Normal pressure readings
- High-pressure anomalies
- Low-pressure anomalies
- Boundary conditions

## Simulation Configuration

The default simulation uses:

| Parameter | Value |
|---|---|
| Equipment ID | ETCH-001 |
| Pressure Setpoint | 50 mTorr |
| Lower Limit | 45 mTorr |
| Upper Limit | 55 mTorr |
| Injected Anomaly | 65 mTorr |

These are hypothetical values used for software development and testing, not validated manufacturing process limits.

## Current Limitations

- The system uses simulated pressure readings.
- Anomaly detection is threshold-based, not machine learning-based.
- Live data generation runs within the Streamlit application.
- The simulator currently models one equipment type.
- Automated tests currently focus on the classification function.

## Project Status

**Functional prototype — under active development.**

Developed as an engineering portfolio project demonstrating Python software development, data processing, monitoring systems, SQL, and automated testing.
