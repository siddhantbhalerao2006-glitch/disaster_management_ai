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
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# SESSION STATE (GENERATE 1000 PEOPLE DATA WITH NAMES)
# ─────────────────────────────────────────────
if "pending_requests" not in st.session_state:
    districts = ["Kothrud","Hadapsar","Pune North","Wakad","Baner","Aundh","Hinjewadi","Viman Nagar"]
    help_types = ["Food + Water","Medical","Evacuation","Shelter"]

    first_names = ["Aarav","Vivaan","Aditya","Vihaan","Arjun","Sai","Krishna","Rohan","Aditi","Ananya","Isha","Meera","Riya","Siddhant","Neha","Rahul","Pooja","Kavita","Suresh","Ramesh"]
    last_names = ["Patil","Sharma","Verma","Gupta","Deshmukh","Nair","Joshi","Kulkarni","Reddy","Mehta","Iyer","Singh"]

    data = []
    total_people = 0
    i = 1

    # generate until ~1000 people total
    while total_people < 1000:
        people = random.randint(2, 15)
        total_people += people

        name = f"{random.choice(first_names)} {random.choice(last_names)}"

        data.append({
            "ID": f"REQ-{i:03d}",
            "Name": name,
            "District": random.choice(districts),
            "People": people,
            "Help Type": random.choice(help_types),
            "Status": random.choice(["Pending","Pending","Dispatched"]),
            "Time": f"{random.randint(8,11)}:{random.randint(0,59):02d}"
        })
        i += 1

    st.session_state.pending_requests = pd.DataFrame(data)

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
        st.title(" AI Disaster Resource Management System ")

        if st.button("📊 Dashboard"):
            st.session_state.nav = "dashboard"

        if st.button("👥 All Requests"):
            st.session_state.nav = "requests"

        if st.button("📦 Inventory"):
            st.session_state.nav = "inventory"

# ─────────────────────────────────────────────
# ADMIN DASHBOARD
# ─────────────────────────────────────────────
def admin_dashboard():
    st.title("📊 Admin Dashboard")

    df = st.session_state.pending_requests

    risk, ratio = get_risk_level(df)

    st.markdown(f"### ⚠️ System Risk Level: **{risk}**")
    st.progress(min(ratio, 1.0))

    st.metric("Total Requests", len(df))
    st.metric("Pending", len(df[df["Status"]=="Pending"]))
    st.metric("Dispatched", len(df[df["Status"]=="Dispatched"]))
    st.metric("People Affected", int(df["People"].sum()))

    st.markdown("---")

    status_filter = st.selectbox("Filter", ["All","Pending","Dispatched"])

    filtered_df = df.copy()
    if status_filter != "All":
        filtered_df = df[df["Status"] == status_filter]

    st.markdown("### 📊 Requests by District")
    st.bar_chart(filtered_df.groupby("District")["People"].sum())

    st.markdown("### 📦 Status Distribution")
    st.bar_chart(df["Status"].value_counts())

    st.markdown("### 📈 People Over Time")
    st.line_chart(df.groupby("Time")["People"].sum())

    st.markdown("### 🗺️ Map View")

    district_coords = {
        "Pune North": (18.55, 73.85),
        "Hadapsar": (18.50, 73.93),
        "Kothrud": (18.50, 73.81),
        "Wakad": (18.60, 73.74),
        "Baner": (18.56, 73.77),
        "Aundh": (18.56, 73.81),
        "Hinjewadi": (18.59, 73.73),
        "Viman Nagar": (18.57, 73.91),
        "Malin Area": (19.03, 73.74),
        "Coastal Belt": (18.90, 72.80),
        "Other": (18.52, 73.85)
    }

    coords = df["District"].map(district_coords)

    if coords.isnull().sum() == 0:
        map_df = pd.DataFrame(coords.tolist(), columns=["lat","lon"])
        st.map(map_df)

    st.markdown("### 💡 Insights")

    if len(df) > 0:
        most_affected = df.groupby("District")["People"].sum().idxmax()
        avg_people = df["People"].mean()

        st.info(f"📍 Most affected district: **{most_affected}**")
        st.info(f"👥 Average people per request: **{avg_people:.2f}**")

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

main()
