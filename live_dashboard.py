import sqlite3
import random
import pandas as pd
import streamlit as st
from database import save_reading
from anomaly_detector import classify_pressure
from fault_injection import inject_fault

# Simulated equipment settings
SETPOINT = 50.0
LOWER_LIMIT = 45.0
UPPER_LIMIT = 55.0

st.set_page_config(page_title="FabWatch Live", layout="wide")

st.title("FabWatch — Live Monitoring")
st.caption("ETCH-001 | Simulated Etching Equipment")

# Remember readings between updates
if "readings" not in st.session_state:
    st.session_state.readings = []

if "second" not in st.session_state:
    st.session_state.second = 0

# Simulation control
if "running" not in st.session_state:
    st.session_state.running = True

# Fault injection state
if "inject_high_pressure" not in st.session_state:
    st.session_state.inject_high_pressure = False

# NEW: Low pressure fault
if "inject_low_pressure" not in st.session_state:
    st.session_state.inject_low_pressure = False

# Sensor failure injection state
if "inject_sensor_failure" not in st.session_state:
    st.session_state.inject_sensor_failure = False

# Automatically update every second
@st.fragment(run_every="1s")
def live_monitor():
    
    # Simulation controls
    col1, col2 = st.columns(2)

    with col1:
        button_label = (
            "Pause Simulation"
            if st.session_state.running
            else "Resume Simulation"
        )

        if st.button(button_label):
            st.session_state.running = not st.session_state.running

    with col2:
        reset_clicked = st.button("Reset Simulation")

    # Reset simulation
    if reset_clicked:
        st.session_state.readings = []
        st.session_state.second = 0
        st.session_state.running = False
        st.session_state.inject_high_pressure = False
        st.session_state.inject_low_pressure = False
        st.session_state.inject_sensor_failure = False

    # High pressure fault button
    if st.button(
        "Inject High Pressure Fault",
        disabled=not st.session_state.running
    ):
        st.session_state.inject_high_pressure = True
        st.session_state.inject_low_pressure = False
        st.session_state.inject_sensor_failure = False
    
    # Low pressure fault button
    if st.button(
        "Inject Low Pressure Fault",
        disabled=not st.session_state.running
    ):
        st.session_state.inject_low_pressure = True
        st.session_state.inject_high_pressure = False
        st.session_state.inject_sensor_failure = False

    # Sensor failure button
    if st.button(
        "Inject Sensor Failure (NaN)",
        disabled=not st.session_state.running
    ):
        st.session_state.inject_sensor_failure = True
        st.session_state.inject_high_pressure = False
        st.session_state.inject_low_pressure = False

    # Generate sensor readings only when running
    if st.session_state.running:
        second = st.session_state.second

        # Generate normal sensor reading
        pressure = round(random.gauss(SETPOINT, 1.5), 2)

        
        # Determine requested fault type
        fault_type = None

        if st.session_state.inject_high_pressure:
            fault_type = "high"

        elif st.session_state.inject_low_pressure:
            fault_type = "low"

        elif st.session_state.inject_sensor_failure:
            fault_type = "sensor_failure"

        # Apply fault using the tested function
        pressure = inject_fault(pressure, fault_type)

        # Clear fault requests after injection
        st.session_state.inject_high_pressure = False
        st.session_state.inject_low_pressure = False
        st.session_state.inject_sensor_failure = False

        # Detect anomalies and validate sensor data
        try:
            status = classify_pressure(
                pressure, LOWER_LIMIT, UPPER_LIMIT
            )

        except ValueError:
            st.error(
                "SENSOR ERROR: Invalid pressure reading. "
                "Measurement skipped."
            )

        else:
            # Save valid sensor readings to SQLite
            save_reading("ETCH-001", pressure, status)

            # Store readings in Session State
            st.session_state.readings.append({
                "second": second,
                "pressure_mTorr": pressure,
                "status": status
            })

        # Advance simulation time
        st.session_state.second += 1

        # Keep latest 60 valid readings
        st.session_state.readings = (
            st.session_state.readings[-60:]
        )


    # Display existing readings, even when paused
    df = pd.DataFrame(st.session_state.readings)

    if df.empty:
        st.info("No sensor readings available.")
        return

    pressure = float(df.iloc[-1]["pressure_mTorr"])
    status = df.iloc[-1]["status"]

    if not st.session_state.running:
        st.info("Simulation PAUSED — displaying last recorded data.")

    anomaly_count = (df["status"] == "WARNING").sum()

    # Display metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Current Pressure", f"{pressure:.2f} mTorr")

    with col2:
        st.metric("Anomalies (Last 60)", int(anomaly_count))

    # Current equipment status
    if status == "WARNING":
        st.error("ETCH-001: ABNORMAL PRESSURE")
    else:
        st.success("ETCH-001: NORMAL")

    # Live pressure chart
    st.subheader("Live Chamber Pressure")

    df["Upper Limit"] = UPPER_LIMIT
    df["Lower Limit"] = LOWER_LIMIT

    st.line_chart(
        df.set_index("second")[
            ["pressure_mTorr", "Upper Limit", "Lower Limit"]
        ]
    )

    st.subheader("Latest Sensor Readings")
    st.dataframe(df.tail(10).iloc[::-1], hide_index=True)

    
# Historical analytics updates independently
@st.fragment(run_every="5s")
def historical_monitor():
    st.subheader("Historical Analytics")

    connection = sqlite3.connect("fabwatch.db")

    try:
        total_readings = connection.execute(
            "SELECT COUNT(*) FROM sensor_readings"
        ).fetchone()[0]

        total_anomalies = connection.execute(
            "SELECT COUNT(*) FROM sensor_readings "
            "WHERE status = 'WARNING'"
        ).fetchone()[0]

        anomaly_history = pd.read_sql_query("""
            SELECT id, equipment_id, pressure, timestamp
            FROM sensor_readings
            WHERE status = 'WARNING'
            ORDER BY id DESC
        """, connection)

    finally:
        connection.close()

    anomaly_rate = (
        total_anomalies / total_readings * 100
        if total_readings > 0 else 0.0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Readings", total_readings)
    col2.metric("Total Anomalies", total_anomalies)
    col3.metric("Anomaly Rate", f"{anomaly_rate:.2f}%")

    st.subheader("Historical Anomaly Records")
    st.dataframe(anomaly_history, hide_index=True)

    st.download_button(
        label="Download Anomaly History",
        data=anomaly_history.to_csv(index=False),
        file_name="fabwatch_anomalies.csv",
        mime="text/csv",
        on_click="ignore"
    )


# Run both monitoring sections
live_monitor()
historical_monitor()
