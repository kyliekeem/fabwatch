import pandas as pd
import streamlit as st

st.set_page_config(page_title="FabWatch", layout="wide")

st.title("FabWatch")
st.caption("Semiconductor Equipment Monitoring Simulator")

# Load data
df = pd.read_csv("sensor_data.csv")

# Detect anomalies
df["anomaly"] = (
    (df["pressure_mTorr"] < 45) |
    (df["pressure_mTorr"] > 55)
)

latest_pressure = df["pressure_mTorr"].iloc[-1]
anomaly_count = int(df["anomaly"].sum())

# Check current equipment status
current_anomaly = bool(df["anomaly"].iloc[-1])

st.subheader("Equipment Status")

if current_anomaly:
    st.error("ETCH-001: WARNING - Abnormal Pressure")
else:
    st.success("ETCH-001: NORMAL - Equipment Stable")

# Dashboard metrics
col1, col2 = st.columns(2)

with col1:
    st.metric("Latest Pressure", f"{latest_pressure:.2f} mTorr")

with col2:
    st.metric("Anomalies Detected", anomaly_count)

if anomaly_count > 0:
    st.warning(f"{anomaly_count} abnormal reading(s) detected!")

# Pressure chart
st.subheader("Chamber Pressure")

df["Upper Limit"] = 55.0
df["Lower Limit"] = 45.0

st.line_chart(
    df.set_index("second")[
        ["pressure_mTorr", "Upper Limit", "Lower Limit"]
    ]
)

# Data table
st.subheader("Sensor Readings")
st.dataframe(df, hide_index=True)
