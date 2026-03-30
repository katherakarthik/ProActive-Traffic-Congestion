import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import random

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Traffic Dashboard", layout="wide")

# ------------------ DARK THEME ------------------
st.markdown("""
<style>
body {background-color: #0e1117; color: white;}
.stApp {background-color: #0e1117;}
h1, h2, h3 {color: #00f2ff;}
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ------------------ LOAD MODEL ------------------
model = pickle.load(open("model.pkl", "rb"))

# ------------------ HELPERS ------------------
def get_signal_time(label):
    return [30, 50, 70, 90][label]

traffic_map_reverse = {
    0: "Low",
    1: "Normal",
    2: "Heavy",
    3: "High"
}

# ------------------ TITLE ------------------
st.markdown(
    "<h1 style='text-align: center; color:#00f2ff;'>🚦 Smart Traffic  Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown("### Real-time traffic prediction & signal optimization")

# ------------------ SIDEBAR ------------------
st.sidebar.header("🚘 Input Traffic Data")

hour = st.sidebar.slider("Hour", 0, 23, 9)
day = st.sidebar.selectbox("Day", [1,2,3,4,5,6,7])
car = st.sidebar.number_input("Car Count", 0, 500, 50)
bike = st.sidebar.number_input("Bike Count", 0, 500, 30)
bus = st.sidebar.number_input("Bus Count", 0, 100, 5)
truck = st.sidebar.number_input("Truck Count", 0, 100, 10)

simulate = st.sidebar.checkbox("🔄 Enable Live Simulation")

total = car + bike + bus + truck

# ------------------ STATIC PREDICTION ------------------
col1, col2 = st.columns(2)

if st.sidebar.button("Predict"):

    if total > 220:
        traffic_label = "High"
        signal = 90
    elif total > 160:
        traffic_label = "Heavy"
        signal = 70
    else:
        features = np.array([[hour, day, car, bike, bus, truck, total]])
        pred = model.predict(features)[0]
        traffic_label = traffic_map_reverse[pred]
        signal = get_signal_time(pred)

    with col1:
        st.subheader("🚦 Prediction Result")

        if traffic_label == "Low":
            st.success(f"🟢 {traffic_label}")
        elif traffic_label == "Normal":
            st.info(f"🟡 {traffic_label}")
        elif traffic_label == "Heavy":
            st.warning(f"🟠 {traffic_label}")
        else:
            st.error(f"🔴 {traffic_label}")

        st.metric("Signal Time", f"{signal} sec")
        st.metric("Total Vehicles", total)

    with col2:
        st.subheader("📊 Vehicle Distribution")

        df_chart = pd.DataFrame({
            "Vehicle": ["Car","Bike","Bus","Truck"],
            "Count": [car, bike, bus, truck]
        })

        st.bar_chart(df_chart.set_index("Vehicle"))

# ------------------ LIVE SIMULATION ------------------
if simulate:

    st.subheader("📡 Live Traffic Simulation")

    chart_placeholder = st.empty()
    metric_placeholder = st.empty()
    trend_placeholder = st.empty()

    signal_history = []

    for i in range(30):

        hour = random.randint(0, 23)
        day = random.randint(1, 7)

        car = random.randint(20, 250)
        bike = random.randint(10, 150)
        bus = random.randint(0, 30)
        truck = random.randint(0, 20)

        total = car + bike + bus + truck

        # Hybrid logic
        if total > 220:
            traffic_label = "High"
            signal = 90
        elif total > 160:
            traffic_label = "Heavy"
            signal = 70
        else:
            features = np.array([[hour, day, car, bike, bus, truck, total]])
            pred = model.predict(features)[0]
            traffic_label = traffic_map_reverse[pred]
            signal = get_signal_time(pred)

        # Update metrics
        metric_placeholder.metric("🚦 Signal Time", f"{signal} sec")

        # Update vehicle chart
        df_live = pd.DataFrame({
            "Vehicle": ["Car", "Bike", "Bus", "Truck"],
            "Count": [car, bike, bus, truck]
        })

        chart_placeholder.bar_chart(df_live.set_index("Vehicle"))

        # Update trend
        signal_history.append(signal)

        trend_df = pd.DataFrame({
            "Step": list(range(len(signal_history))),
            "Signal": signal_history
        })

        trend_placeholder.line_chart(trend_df.set_index("Step"))

        st.write(f"Hour: {hour} | Traffic: {traffic_label} | Total: {total}")

        time.sleep(1)

# ------------------ FEATURE IMPORTANCE ------------------
st.subheader("🧠 Feature Importance")

try:
    importance = model.feature_importances_
    features = ["Hour","Day","Car","Bike","Bus","Truck","Total"]

    fig, ax = plt.subplots()
    ax.barh(features, importance)
    ax.set_title("Feature Importance")

    st.pyplot(fig)

except:
    st.warning("Feature importance not available")

# ------------------ TRAFFIC TREND ------------------
st.subheader("📈 Traffic Signal Trend")

hours = list(range(24))
signal_times = [30,30,30,30,30,30,50,70,90,90,70,50,
                50,70,90,90,70,50,50,70,90,90,50,30]

trend_df = pd.DataFrame({
    "Hour": hours,
    "Signal Time": signal_times
})

st.line_chart(trend_df.set_index("Hour"))