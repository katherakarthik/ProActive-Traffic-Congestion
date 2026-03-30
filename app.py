import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import random

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Traffic AI Dashboard", layout="wide")

# ------------------ GLOBAL STYLES ------------------
st.markdown("""
<style>

/* Hide Streamlit header */
header {visibility: hidden;}

/* Remove top padding */
.block-container {
    padding-top: 1rem;
}

/* App background */
.stApp {
    background-color: #0e1117;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161b22;
}

/* Sidebar labels */
[data-testid="stSidebar"] label {
    color: white !important;
    font-weight: 600;
}

/* Sidebar checkbox text */
[data-testid="stSidebar"] span {
    color: white !important;
}

/* Inputs */
input, select {
    background-color: #0e1117 !important;
    color: white !important;
    border: 1px solid #00ffff !important;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}

/* Headings */
.heading {
    color:#00ffff;
    text-shadow:0 0 8px #00ffff;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 8px;
}

/* General text */
html, body, [class*="css"] {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.markdown("""
<h1 style='text-align:center;color:#00ffff;
text-shadow:0 0 10px #00ffff;'>🚦 Smart Traffic Dashboard</h1>
""", unsafe_allow_html=True)

st.markdown(
    "<h3 style='text-align:center;color:white;'>Real-time traffic prediction & signal optimization</h3>",
    unsafe_allow_html=True
)

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

def signal_color(label):
    return {
        "Low": "🟢",
        "Normal": "🟡",
        "Heavy": "🟠",
        "High": "🔴"
    }[label]

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

# ------------------ PREDICTION ------------------
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

    # ---------- CARD 1 ----------
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("<h2 class='heading'>🚦 Prediction Result</h2>", unsafe_allow_html=True)

        st.markdown(f"""
        <p style='font-size:22px;'>{signal_color(traffic_label)} {traffic_label}</p>
        <h3>Signal Time: {signal} sec</h3>
        <h3>Total Vehicles: {total}</h3>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------- CARD 2 ----------
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("<h2 class='heading'>📊 Vehicle Distribution</h2>", unsafe_allow_html=True)

        df_chart = pd.DataFrame({
            "Vehicle": ["Car","Bike","Bus","Truck"],
            "Count": [car, bike, bus, truck]
        })

        st.bar_chart(df_chart.set_index("Vehicle"))

        st.markdown('</div>', unsafe_allow_html=True)

# ------------------ LIVE SIMULATION ------------------
if simulate:

    st.markdown("<h2 class='heading'>📡 Live Traffic Simulation</h2>", unsafe_allow_html=True)

    chart_placeholder = st.empty()
    trend_placeholder = st.empty()

    signal_history = []

    for i in range(20):

        car = random.randint(20, 250)
        bike = random.randint(10, 150)
        bus = random.randint(0, 30)
        truck = random.randint(0, 20)

        total = car + bike + bus + truck

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

        df_live = pd.DataFrame({
            "Vehicle": ["Car","Bike","Bus","Truck"],
            "Count": [car, bike, bus, truck]
        })

        chart_placeholder.bar_chart(df_live.set_index("Vehicle"))

        signal_history.append(signal)

        trend_df = pd.DataFrame({
            "Step": list(range(len(signal_history))),
            "Signal": signal_history
        })

        trend_placeholder.line_chart(trend_df.set_index("Step"))

        st.markdown(
            f"<p style='color:white;'>Traffic: {traffic_label} | Signal: {signal}</p>",
            unsafe_allow_html=True
        )

        time.sleep(1)

# ------------------ FEATURE IMPORTANCE ------------------
st.markdown("<h2 class='heading'>🧠 Feature Importance</h2>", unsafe_allow_html=True)

try:
    importance = model.feature_importances_
    features = ["Hour","Day","Car","Bike","Bus","Truck","Total"]

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')

    ax.barh(features, importance, color='#00ffff')
    ax.tick_params(colors='white')
    ax.set_title("Feature Importance", color='white')

    st.pyplot(fig)

except:
    st.warning("Feature importance not available")

# ------------------ TRAFFIC TREND ------------------
st.markdown("<h2 class='heading'>📈 Traffic Signal Trend</h2>", unsafe_allow_html=True)

hours = list(range(24))
signal_times = [30,30,30,30,30,30,50,70,90,90,70,50,
                50,70,90,90,70,50,50,70,90,90,50,30]

fig, ax = plt.subplots()
fig.patch.set_facecolor('#0e1117')
ax.set_facecolor('#0e1117')

ax.plot(hours, signal_times, color='#00ffff')
ax.tick_params(colors='white')
ax.set_title("Traffic Signal Trend", color='white')

st.pyplot(fig)