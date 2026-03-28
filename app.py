import streamlit as st
import pandas as pd
from datetime import datetime
import random
import numpy as np

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DisasterNet — Relief Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "pending_requests" not in st.session_state:
    st.session_state.pending_requests = pd.DataFrame([
        {"ID":"REQ-001","Name":"Sunita Devi","District":"Kothrud","People":6,"Help Type":"Food + Water","Status":"Pending","Time":"09:12"},
        {"ID":"REQ-002","Name":"Ramesh Patil","District":"Hadapsar","People":3,"Help Type":"Medical","Status":"Dispatched","Time":"09:45"},
        {"ID":"REQ-003","Name":"Kavita Joshi","District":"Pune North","People":12,"Help Type":"Evacuation","Status":"Pending","Time":"10:03"},
        {"ID":"REQ-004","Name":"Suresh Nair","District":"Wakad","People":4,"Help Type":"Shelter","Status":"Pending","Time":"10:21"},
    ])

if "dispatches" not in st.session_state:
    st.session_state.dispatches = []

# ─────────────────────────────────────────────
# HELPER: RISK LEVEL
# ─────────────────────────────────────────────
def get_risk_level(df):
    pending = len(df[df["Status"] == "Pending"])
    total = len(df)

    if total == 0:
        return "Low", 0

    ratio = pending / total

    if ratio > 0.6:
        return "Critical", ratio
    elif ratio > 0.3:
        return "High", ratio
    elif ratio > 0.1:
        return "Medium", ratio
    else:
        return "Low", ratio

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.title("🛡️ DisasterNet")

        if st.button("📊 Dashboard"):
            st.session_state.nav = "dashboard"

        if st.button("👥 All Requests"):
            st.session_state.nav = "requests"

        if st.button("📦 Inventory"):
            st.session_state.nav = "inventory"

# ─────────────────────────────────────────────
# ADMIN DASHBOARD (FINAL UPGRADED)
# ─────────────────────────────────────────────
def admin_dashboard():
    st.title("📊 Admin Dashboard")

    df = st.session_state.pending_requests

    # ── RISK LEVEL ──
    risk, ratio = get_risk_level(df)

    st.markdown(f"### ⚠️ System Risk Level: **{risk}**")
    st.progress(min(ratio, 1.0))

    # ── STATS ──
    st.metric("Total Requests", len(df))
    st.metric("Pending", len(df[df["Status"]=="Pending"]))
    st.metric("Dispatched", len(df[df["Status"]=="Dispatched"]))
    st.metric("People Affected", int(df["People"].sum()))

    st.markdown("---")

    # ── FILTER ──
    status_filter = st.selectbox("Filter", ["All","Pending","Dispatched"])

    filtered_df = df.copy()
    if status_filter != "All":
        filtered_df = df[df["Status"] == status_filter]

    # ── CHARTS ──
    st.markdown("### 📊 Requests by District")
    st.bar_chart(filtered_df.groupby("District")["People"].sum())

    st.markdown("### 📌 Status Distribution")
    st.bar_chart(df["Status"].value_counts())

    st.markdown("### 📈 People Over Time")
    st.line_chart(df.groupby("Time")["People"].sum())

    # ── MAP ──
    st.markdown("### 🗺️ Map View")

    district_coords = {
        "Pune North": (18.55, 73.85),
        "Hadapsar": (18.50, 73.93),
        "Kothrud": (18.50, 73.81),
        "Wakad": (18.60, 73.74),
        "Malin Area": (19.03, 73.74),
        "Coastal Belt": (18.90, 72.80),
        "Other": (18.52, 73.85)
    }

    coords = df["District"].map(district_coords)

    if coords.isnull().sum() == 0:
        map_df = pd.DataFrame(coords.tolist(), columns=["lat","lon"])
        st.map(map_df)

    # ── INSIGHTS ──
    st.markdown("### 💡 Insights")

    if len(df) > 0:
        most_affected = df.groupby("District")["People"].sum().idxmax()
        avg_people = df["People"].mean()

        st.info(f"📍 Most affected district: **{most_affected}**")
        st.info(f"👥 Average people per request: **{avg_people:.2f}**")

    # ── TABLE ──
    st.markdown("### 📋 Data")
    st.dataframe(filtered_df, use_container_width=True)

# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
def main():
    render_sidebar()

    if "nav" not in st.session_state:
        st.session_state.nav = "dashboard"

    if st.session_state.nav == "dashboard":
        admin_dashboard()
    elif st.session_state.nav == "requests":
        st.dataframe(st.session_state.pending_requests)
    elif st.session_state.nav == "inventory":
        st.info("Inventory page (you can expand this)")

# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────
main()