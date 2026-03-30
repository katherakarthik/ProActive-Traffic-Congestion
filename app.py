import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
import random
from pathlib import Path

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Traffic Dashboard",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CROSS-BROWSER ROBUST CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

/* ── Reset & Base ── */
header { visibility: hidden; }
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1400px;
}

/* ── App Background ── */
.stApp {
    background-color: #080c14 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Background grid pattern ── */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(0,229,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,229,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #0d1420 !important;
    border-right: 1px solid rgba(0, 229, 255, 0.15) !important;
}

/* Force ALL sidebar text white — fixes Brave / Edge / mobile */
[data-testid="stSidebar"],
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Sidebar header */
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #00e5ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 1px;
}

/* ── Slider ── */
[data-testid="stSlider"] {
    padding: 4px 0;
}
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background-color: #00e5ff !important;
    border-color: #00e5ff !important;
}
[data-testid="stSlider"] [class*="StyledThumb"] {
    background-color: #00e5ff !important;
    border-color: #00e5ff !important;
    box-shadow: 0 0 8px rgba(0,229,255,0.6) !important;
}
[data-testid="stSlider"] [class*="StyledTrack"] {
    background-color: rgba(0,229,255,0.25) !important;
}
[data-testid="stSlider"] [class*="StyledTrack"]:first-child {
    background-color: #00e5ff !important;
}

/* ── Number Input ── */
[data-testid="stNumberInput"] input {
    background-color: #111827 !important;
    color: #ffffff !important;
    border: 1px solid rgba(0, 198, 255, 0.4) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #00e5ff !important;
    box-shadow: 0 0 0 2px rgba(0,229,255,0.2) !important;
}
[data-testid="stNumberInput"] button {
    background-color: #1e293b !important;
    color: #00e5ff !important;
    border: 1px solid rgba(0,198,255,0.3) !important;
}
[data-testid="stNumberInput"] button:hover {
    background-color: rgba(0,229,255,0.15) !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background-color: #111827 !important;
    color: #ffffff !important;
    border: 1px solid rgba(0, 198, 255, 0.4) !important;
    border-radius: 8px !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #00e5ff !important;
    box-shadow: 0 0 0 2px rgba(0,229,255,0.2) !important;
}
/* Dropdown options list */
[data-testid="stSelectbox"] ul {
    background-color: #111827 !important;
    border: 1px solid rgba(0,229,255,0.3) !important;
    border-radius: 8px !important;
}
[data-testid="stSelectbox"] li {
    color: #e2e8f0 !important;
}
[data-testid="stSelectbox"] li:hover {
    background-color: rgba(0,229,255,0.1) !important;
}
/* Selectbox arrow icon */
[data-testid="stSelectbox"] svg {
    fill: #00e5ff !important;
}

/* ── Checkbox ── */
[data-testid="stCheckbox"] span {
    color: #e2e8f0 !important;
    font-size: 14px !important;
}
[data-testid="stCheckbox"] input:checked + div {
    background-color: #00e5ff !important;
    border-color: #00e5ff !important;
}

/* ── Predict Button ── */
.stButton > button {
    background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
    padding: 0.6rem 1.2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(0, 114, 255, 0.35) !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 28px rgba(0, 198, 255, 0.55) !important;
    opacity: 0.95 !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0d1a2d 0%, #111827 100%) !important;
    border: 1px solid rgba(0, 229, 255, 0.2) !important;
    border-radius: 14px !important;
    padding: 20px 24px !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00c6ff, #0072ff);
}
[data-testid="stMetric"] label,
[data-testid="stMetric"] [data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #00e5ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
}

/* ── Main text ── */
.stApp p,
.stApp span:not([class*="stMetric"]),
.stApp li {
    color: #cbd5e1;
}

/* ── Divider ── */
hr {
    border-color: rgba(0,229,255,0.1) !important;
    margin: 1rem 0 !important;
}

/* ── Warning / Info ── */
.stAlert {
    border-radius: 10px !important;
    border-left-color: #00e5ff !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] {
    color: #00e5ff !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #080c14; }
::-webkit-scrollbar-thumb { background: rgba(0,229,255,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,229,255,0.6); }

</style>
""", unsafe_allow_html=True)


# ── HELPERS ───────────────────────────────────────────────────────────────────
TRAFFIC_MAP = {0: "Low", 1: "Normal", 2: "Heavy", 3: "High"}
SIGNAL_MAP  = {0: 30,    1: 50,       2: 70,      3: 90}
STATUS_COLORS = {
    "Low":    ("#22c55e", "🟢"),
    "Normal": ("#eab308", "🟡"),
    "Heavy":  ("#f97316", "🟠"),
    "High":   ("#ef4444", "🔴"),
}

def classify(hour, day, car, bike, bus, truck, total, model):
    if total > 220:
        return "High", 90
    elif total > 160:
        return "Heavy", 70
    features = np.array([[hour, day, car, bike, bus, truck, total]])
    pred = model.predict(features)[0]
    return TRAFFIC_MAP[pred], SIGNAL_MAP[pred]

def make_dark_fig(figsize=(6, 3)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor('#0d1420')
    ax.set_facecolor('#0d1420')
    for spine in ax.spines.values():
        spine.set_edgecolor((0, 0.898, 1.0, 0.15))
    ax.tick_params(colors='#94a3b8', labelsize=10)
    ax.xaxis.label.set_color('#94a3b8')
    ax.yaxis.label.set_color('#94a3b8')
    return fig, ax


# ── MODEL LOAD ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model_path = Path(__file__).parent / "model.pkl"
    with open(model_path, "rb") as f:
        return pickle.load(f)

try:
    model = load_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.warning(f"⚠️ Could not load model.pkl — running in demo mode. ({e})")


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 0.5rem 0 1.5rem 0;">
    <div style="font-size: 13px; letter-spacing: 4px; color: #00e5ff; opacity: 0.7;
                font-family: 'Rajdhani', sans-serif; text-transform: uppercase;
                margin-bottom: 6px;">
        AI-POWERED SYSTEM
    </div>
    <h1 style="font-family: 'Rajdhani', sans-serif; font-size: clamp(2rem, 5vw, 3.2rem);
               font-weight: 700; color: #ffffff; margin: 0; line-height: 1;
               letter-spacing: 2px;">
        🚦 SMART TRAFFIC DASHBOARD
    </h1>
    <p style="color: #64748b; font-size: 15px; margin-top: 8px; letter-spacing: 0.5px;">
        Real-time prediction & adaptive signal optimization
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <h2 style="font-family:'Rajdhani',sans-serif; font-size:22px; font-weight:700;
               color:#00e5ff; letter-spacing:2px; margin-bottom:4px;">
        ⚙️ INPUT PARAMETERS
    </h2>
    <p style="font-size:12px; color:#64748b; margin-bottom:16px;">
        Configure traffic snapshot below
    </p>
    """, unsafe_allow_html=True)

    st.markdown("**🕐 Time**")
    hour = st.slider("Hour of Day", 0, 23, 9, help="0 = midnight, 23 = 11 PM")
    day  = st.selectbox("Day of Week", [1, 2, 3, 4, 5, 6, 7],
                        format_func=lambda x: ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][x-1])

    st.divider()
    st.markdown("**🚗 Vehicle Counts**")
    car   = st.number_input("Cars",   min_value=0, max_value=500, value=50, step=5)
    bike  = st.number_input("Bikes",  min_value=0, max_value=500, value=30, step=5)
    bus   = st.number_input("Buses",  min_value=0, max_value=100, value=5,  step=1)
    truck = st.number_input("Trucks", min_value=0, max_value=100, value=10, step=1)

    total = car + bike + bus + truck

    st.divider()

    # Live load indicator
    load_pct = min(int((total / 300) * 100), 100)
    load_color = "#22c55e" if load_pct < 40 else "#eab308" if load_pct < 70 else "#ef4444"
    st.markdown(f"""
    <div style="margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <span style="font-size:12px; color:#94a3b8; letter-spacing:1px;">ROAD LOAD</span>
            <span style="font-size:12px; color:{load_color}; font-weight:700;">{load_pct}%</span>
        </div>
        <div style="background:#1e293b; border-radius:999px; height:6px; overflow:hidden;">
            <div style="width:{load_pct}%; height:100%; border-radius:999px;
                        background: linear-gradient(90deg, #22c55e, {load_color});
                        transition: width 0.4s ease;"></div>
        </div>
        <div style="font-size:11px; color:#475569; margin-top:4px;">
            Total vehicles: <strong style="color:#e2e8f0;">{total}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    simulate = st.checkbox("🔄 Enable Live Simulation", value=False)
    predict  = st.button("🚀 PREDICT", use_container_width=True)


# ── PREDICTION SECTION ────────────────────────────────────────────────────────
if predict:
    if not model_loaded:
        # Demo fallback when model.pkl is absent
        label  = random.choice(["Low", "Normal", "Heavy", "High"])
        signal = {"Low": 30, "Normal": 50, "Heavy": 70, "High": 90}[label]
    else:
        label, signal = classify(hour, day, car, bike, bus, truck, total, model)

    color, icon = STATUS_COLORS[label]

    st.session_state["last_prediction"] = {
        "label": label, "signal": signal,
        "car": car, "bike": bike, "bus": bus, "truck": truck, "total": total,
    }

# Display last prediction if available
if "last_prediction" in st.session_state:
    p = st.session_state["last_prediction"]
    label, signal = p["label"], p["signal"]
    color, icon   = STATUS_COLORS[label]

    # ── KPI Row ──
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Traffic Status", f"{icon} {label}")
    with k2:
        st.metric("Signal Time", f"{signal} sec")
    with k3:
        st.metric("Total Vehicles", str(p["total"]))
    with k4:
        efficiency = max(0, 100 - int((signal / 90) * 60))
        st.metric("Flow Efficiency", f"{efficiency}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts Row ──
    c1, c2 = st.columns([1, 1], gap="large")

    with c1:
        st.markdown("""
        <div style="font-family:'Rajdhani',sans-serif; font-size:18px; font-weight:700;
                    color:#00e5ff; letter-spacing:1px; margin-bottom:12px;">
            📊 VEHICLE DISTRIBUTION
        </div>
        """, unsafe_allow_html=True)

        fig, ax = make_dark_fig(figsize=(5, 3.2))
        vehicles = ["Car", "Bike", "Bus", "Truck"]
        counts   = [p["car"], p["bike"], p["bus"], p["truck"]]
        bar_colors = ["#00c6ff", "#0072ff", "#6366f1", "#8b5cf6"]
        bars = ax.bar(vehicles, counts, color=bar_colors, width=0.55, zorder=3,
                      edgecolor='none')

        # Value labels on bars
        for bar, val in zip(bars, counts):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                        str(val), ha='center', va='bottom',
                        color='#e2e8f0', fontsize=10, fontweight='600')

        ax.set_ylabel("Count", color='#64748b', fontsize=10)
        ax.yaxis.grid(True, color=(0.392, 0.455, 0.549, 0.15), linestyle='--', zorder=0)
        ax.set_axisbelow(True)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with c2:
        st.markdown("""
        <div style="font-family:'Rajdhani',sans-serif; font-size:18px; font-weight:700;
                    color:#00e5ff; letter-spacing:1px; margin-bottom:12px;">
            🎯 TRAFFIC COMPOSITION
        </div>
        """, unsafe_allow_html=True)

        fig, ax = make_dark_fig(figsize=(5, 3.2))
        if p["total"] > 0:
            sizes  = [p["car"], p["bike"], p["bus"], p["truck"]]
            labels = ["Cars", "Bikes", "Buses", "Trucks"]
            pcolors = ["#00c6ff", "#0072ff", "#6366f1", "#8b5cf6"]
            wedges, texts, autotexts = ax.pie(
                sizes, labels=None, colors=pcolors,
                autopct=lambda pct: f'{pct:.1f}%' if pct > 3 else '',
                startangle=90, pctdistance=0.78,
                wedgeprops=dict(edgecolor='#080c14', linewidth=2, width=0.65)
            )
            for at in autotexts:
                at.set_color('#ffffff')
                at.set_fontsize(9)
                at.set_fontweight('600')
            patches = [mpatches.Patch(color=c, label=l) for c, l in zip(pcolors, labels)]
            ax.legend(handles=patches, loc='lower center', bbox_to_anchor=(0.5, -0.12),
                      ncol=4, fontsize=8, frameon=False,
                      labelcolor='#94a3b8')
        else:
            ax.text(0.5, 0.5, "No vehicles", ha='center', va='center',
                    color='#475569', transform=ax.transAxes, fontsize=12)
            ax.axis('off')

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.divider()


# ── FEATURE IMPORTANCE ────────────────────────────────────────────────────────
st.markdown("""
<div style="font-family:'Rajdhani',sans-serif; font-size:22px; font-weight:700;
            color:#00e5ff; letter-spacing:2px; margin-bottom:16px;">
    🧠 FEATURE IMPORTANCE
</div>
""", unsafe_allow_html=True)

fi_col, trend_col = st.columns([1, 1], gap="large")

with fi_col:
    if model_loaded:
        try:
            importance = model.feature_importances_
            feat_names = ["Hour", "Day", "Car", "Bike", "Bus", "Truck", "Total"]
            sorted_idx = np.argsort(importance)
            fig, ax = make_dark_fig(figsize=(5, 3.5))
            grad_colors = plt.cm.cool(np.linspace(0.3, 0.9, len(feat_names)))
            bars = ax.barh(
                [feat_names[i] for i in sorted_idx],
                importance[sorted_idx],
                color=[grad_colors[i] for i in range(len(sorted_idx))],
                height=0.6, edgecolor='none', zorder=3
            )
            ax.xaxis.grid(True, color=(0.392, 0.455, 0.549, 0.15), linestyle='--', zorder=0)
            ax.set_axisbelow(True)
            ax.set_xlabel("Importance Score", color='#64748b', fontsize=10)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            for bar, val in zip(bars, importance[sorted_idx]):
                ax.text(val + 0.002, bar.get_y() + bar.get_height()/2,
                        f'{val:.3f}', va='center', color='#94a3b8', fontsize=8)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
        except Exception:
            st.info("Feature importance not available for this model type.")
    else:
        st.info("Load a valid model.pkl to see feature importance.")

with trend_col:
    st.markdown("""
    <div style="font-family:'Rajdhani',sans-serif; font-size:18px; font-weight:700;
                color:#00e5ff; letter-spacing:1px; margin-bottom:4px;">
        📈 SIGNAL TIMING — 24H TREND
    </div>
    """, unsafe_allow_html=True)

    hours_list   = list(range(24))
    signal_times = [30,30,30,30,30,30,50,70,90,90,70,50,
                    50,70,90,90,70,50,50,70,90,90,50,30]

    fig, ax = make_dark_fig(figsize=(5, 3.5))
    ax.fill_between(hours_list, signal_times,
                    alpha=0.15, color='#00e5ff')
    ax.plot(hours_list, signal_times,
            color='#00e5ff', linewidth=2, zorder=3)
    ax.scatter(hours_list, signal_times,
               color='#0072ff', s=30, zorder=4, edgecolors='#00e5ff', linewidths=0.8)

    # Highlight current hour
    if 0 <= hour <= 23:
        ax.axvline(x=hour, color='#f97316', linestyle='--', linewidth=1.5, alpha=0.7, zorder=5)
        ax.text(hour + 0.3, max(signal_times) - 5, f'Now ({hour}:00)',
                color='#f97316', fontsize=8)

    ax.set_xlabel("Hour", color='#64748b', fontsize=10)
    ax.set_ylabel("Signal Time (sec)", color='#64748b', fontsize=10)
    ax.set_xticks([0, 6, 12, 18, 23])
    ax.set_xticklabels(['12am', '6am', '12pm', '6pm', '11pm'])
    ax.yaxis.grid(True, color=(0.392, 0.455, 0.549, 0.15), linestyle='--', zorder=0)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ── LIVE SIMULATION ───────────────────────────────────────────────────────────
if simulate:
    st.divider()
    st.markdown("""
    <div style="font-family:'Rajdhani',sans-serif; font-size:22px; font-weight:700;
                color:#00e5ff; letter-spacing:2px; margin-bottom:16px;">
        📡 LIVE TRAFFIC SIMULATION
    </div>
    """, unsafe_allow_html=True)

    sim_bar   = st.empty()
    sim_line  = st.empty()
    sim_badge = st.empty()

    signal_history = []
    STEPS = 20

    for i in range(STEPS):
        s_car   = random.randint(20, 250)
        s_bike  = random.randint(10, 150)
        s_bus   = random.randint(0, 30)
        s_truck = random.randint(0, 20)
        s_total = s_car + s_bike + s_bus + s_truck

        if model_loaded:
            s_label, s_signal = classify(hour, day, s_car, s_bike, s_bus, s_truck, s_total, model)
        else:
            s_label = random.choice(["Low", "Normal", "Heavy", "High"])
            s_signal = {"Low": 30, "Normal": 50, "Heavy": 70, "High": 90}[s_label]

        signal_history.append(s_signal)
        s_color, s_icon = STATUS_COLORS[s_label]

        with sim_bar.container():
            fig, ax = make_dark_fig(figsize=(6, 2.8))
            veh    = ["Car", "Bike", "Bus", "Truck"]
            vcounts = [s_car, s_bike, s_bus, s_truck]
            ax.bar(veh, vcounts, color=["#00c6ff","#0072ff","#6366f1","#8b5cf6"],
                   width=0.5, zorder=3, edgecolor='none')
            ax.yaxis.grid(True, color=(0.392, 0.455, 0.549, 0.15), linestyle='--', zorder=0)
            ax.set_axisbelow(True)
            ax.set_title(f"Step {i+1}/{STEPS}", color='#64748b', fontsize=10, pad=6)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        with sim_line.container():
            fig, ax = make_dark_fig(figsize=(6, 2.5))
            ax.plot(range(len(signal_history)), signal_history,
                    color='#00e5ff', linewidth=2, marker='o', markersize=4, zorder=3)
            ax.fill_between(range(len(signal_history)), signal_history,
                            alpha=0.12, color='#00e5ff')
            ax.set_ylabel("Signal (sec)", color='#64748b', fontsize=10)
            ax.set_xlabel("Step", color='#64748b', fontsize=10)
            ax.yaxis.grid(True, color=(0.392, 0.455, 0.549, 0.15), linestyle='--', zorder=0)
            ax.set_axisbelow(True)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        sim_badge.markdown(f"""
        <div style="display:inline-flex; align-items:center; gap:10px;
                    background:#0d1a2d; border:1px solid rgba(0,229,255,0.2);
                    border-radius:10px; padding:10px 20px; margin:8px 0;">
            <span style="font-size:22px;">{s_icon}</span>
            <div>
                <div style="font-family:'Rajdhani',sans-serif; font-size:18px;
                            font-weight:700; color:{s_color};">{s_label}</div>
                <div style="font-size:12px; color:#64748b;">
                    Signal: <strong style="color:#e2e8f0;">{s_signal}s</strong> &nbsp;|&nbsp;
                    Vehicles: <strong style="color:#e2e8f0;">{s_total}</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(1)

    st.success("✅ Simulation complete .") 


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center; padding:12px 0 4px 0;">
    <span style="font-size:12px; color:#334155; letter-spacing:2px;">
        SMART TRAFFIC DASHBOARD &nbsp;·&nbsp; AI-POWERED SIGNAL OPTIMIZATION
    </span>
</div>
""", unsafe_allow_html=True)