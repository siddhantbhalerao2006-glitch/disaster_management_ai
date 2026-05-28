import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go
import os
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Disaster Management System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# MODERN UI
# =========================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to bottom right,#050816,#0f172a);
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#0b1120;
    border-right:1px solid #1e293b;
}

/* Main cards */
.card {
    background: rgba(255,255,255,0.05);
    padding:20px;
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.08);
    box-shadow:0 8px 25px rgba(0,0,0,0.4);
    margin-bottom:20px;
}

/* Hero */
.hero {
    padding:35px;
    border-radius:20px;
    background: linear-gradient(90deg,#ff3b3b,#2563eb);
    text-align:center;
    margin-bottom:25px;
}

/* Buttons */
.stButton > button {
    width:100%;
    background:linear-gradient(90deg,#ff3b3b,#ff7300);
    color:white;
    border:none;
    border-radius:12px;
    padding:12px;
    font-weight:bold;
    transition:0.3s;
}

.stButton > button:hover{
    transform:scale(1.03);
    box-shadow:0 0 15px rgba(255,0,0,0.5);
}

/* Metrics */
[data-testid="metric-container"]{
    background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    padding:15px;
    border-radius:15px;
}

/* Alert ticker */
.ticker {
    background:#111827;
    padding:12px;
    border-radius:10px;
    color:#ff4d4d;
    font-weight:bold;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================
st.markdown("""
<div class="hero">
<h1>🚨 AI DISASTER MANAGEMENT SYSTEM</h1>
<h3>Real-Time Emergency Intelligence Dashboard</h3>
<p>AI Powered Disaster Monitoring • SOS Tracking • Emergency Coordination</p>
</div>
""", unsafe_allow_html=True)

# =========================
# LIVE ALERT TICKER
# =========================
st.markdown("""
<div class="ticker">
🚨 Heavy Rainfall Alert • 🌊 Flood Risk Increased • 🚒 Fire Emergency Monitoring Active
</div>
""", unsafe_allow_html=True)

# =========================
# DATA FILE
# =========================
DATA_FILE = "sos_data.csv"

# =========================
# LOAD DATA
# =========================
def load_data():

    columns = [
        "ID",
        "Name",
        "District",
        "People",
        "Type",
        "Priority",
        "Status",
        "Image",
        "Time",
        "lat",
        "lon"
    ]

    if os.path.exists(DATA_FILE):

        df = pd.read_csv(DATA_FILE)

        df.columns = df.columns.str.strip()

        for col in columns:

            if col not in df.columns:

                if col in ["People", "lat", "lon"]:
                    df[col] = 0
                else:
                    df[col] = ""

        text_cols = [
            "ID",
            "Name",
            "District",
            "Type",
            "Priority",
            "Status",
            "Image",
            "Time"
        ]

        df[text_cols] = df[text_cols].fillna("")

        df["People"] = pd.to_numeric(
            df["People"],
            errors="coerce"
        ).fillna(0)

        df["lat"] = pd.to_numeric(
            df["lat"],
            errors="coerce"
        ).fillna(0)

        df["lon"] = pd.to_numeric(
            df["lon"],
            errors="coerce"
        ).fillna(0)

        return df

    return pd.DataFrame(columns=columns)

# =========================
# SAVE DATA
# =========================
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# =========================
# SESSION
# =========================
if "data" not in st.session_state:
    st.session_state.data = load_data()

# =========================
# LOCATION MAP
# =========================
DISTRICT_MAP = {
    "Kothrud": (18.5074, 73.8077),
    "Hadapsar": (18.5089, 73.9259),
    "Wakad": (18.5987, 73.7607),
    "Baner": (18.5590, 73.7787),
    "Aundh": (18.5580, 73.8075)
}

# =========================
# AI RISK ENGINE
# =========================
def risk_level(df):

    if len(df) == 0:
        return "LOW 🟢"

    pending = len(df[df["Status"] == "Pending"])

    ratio = pending / len(df)

    if ratio > 0.6:
        return "CRITICAL 🔴"

    elif ratio > 0.3:
        return "HIGH 🟠"

    elif ratio > 0.1:
        return "MEDIUM 🟡"

    return "LOW 🟢"

# =========================
# AI SUPPLY PREDICTION
# =========================
def predict_supplies(dtype, people, priority):

    supplies = []

    if dtype == "Flood":

        supplies.extend([
            "Drinking Water 💧",
            "Food Packets 🍱",
            "Rescue Boats 🚤",
            "Life Jackets 🦺"
        ])

    elif dtype == "Fire":

        supplies.extend([
            "Fire Trucks 🚒",
            "Burn Medical Kits 🩹",
            "Oxygen Cylinders 🫁",
            "Fire Extinguishers 🧯"
        ])

    elif dtype == "Earthquake":

        supplies.extend([
            "Emergency Tents ⛺",
            "Medical Teams 🚑",
            "Rescue Equipment ⛑️",
            "Food Supplies 🍞"
        ])

    elif dtype == "Accident":

        supplies.extend([
            "Ambulance 🚑",
            "First Aid Kits 🩹",
            "Traffic Control 🚧"
        ])

    if people > 20:
        supplies.append("Extra Food Supplies 🍱")

    if people > 50:
        supplies.append("Large Rescue Team 👨‍🚒")

    if priority == "High":
        supplies.append("Immediate Helicopter Support 🚁")

    return supplies

# =========================
# BUILD MAP
# =========================
def build_map(df):

    fig = go.Figure()

    if not df.empty:

        fig.add_trace(go.Scattermapbox(
            lat=df["lat"],
            lon=df["lon"],
            mode="markers",
            marker=dict(
                size=df["People"].astype(int) * 2,
                color=df["Priority"].map({
                    "High": "red",
                    "Medium": "orange",
                    "Low": "green"
                })
            ),
            text=df["District"] + " | " + df["Type"]
        ))

    fig.update_layout(
        mapbox_style="carto-darkmatter",
        mapbox=dict(
            center=dict(lat=18.55, lon=73.85),
            zoom=10
        ),
        height=500,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig

# =========================
# SAFE IMAGE DISPLAY
# =========================
def show_image(row):

    if (
        "Image" in row
        and pd.notna(row["Image"])
        and row["Image"] != ""
        and os.path.exists(row["Image"])
    ):
        st.image(row["Image"], use_container_width=True)

# =========================
# USER PANEL
# =========================
def user_panel():

    st.markdown("## 👤 Citizen Emergency Dashboard")

    with st.form("sos_form"):

        st.markdown("### 🚨 Send Emergency SOS")

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input("👤 Your Name")

            district = st.selectbox(
                "📍 Location",
                list(DISTRICT_MAP.keys())
            )

            dtype = st.selectbox(
                "🔥 Disaster Type",
                ["Fire", "Flood", "Earthquake", "Accident"]
            )

        with col2:

            people = st.slider(
                "👥 People Affected",
                1, 100, 5
            )

            priority = st.selectbox(
                "⚠️ Priority",
                ["Low", "Medium", "High"]
            )

            uploaded_file = st.file_uploader(
                "📸 Upload Disaster Image",
                type=["png", "jpg", "jpeg"]
            )

        submit = st.form_submit_button("🚨 SEND SOS ALERT")

        if submit:

            image_path = ""

            if uploaded_file is not None:

                os.makedirs("uploads", exist_ok=True)

                image_path = f"uploads/{uploaded_file.name}"

                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            new_data = {
                "ID": f"SOS-{random.randint(1000,9999)}",
                "Name": name,
                "District": district,
                "People": people,
                "Type": dtype,
                "Priority": priority,
                "Status": "Pending",
                "Image": image_path,
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "lat": DISTRICT_MAP[district][0],
                "lon": DISTRICT_MAP[district][1]
            }

            st.session_state.data = pd.concat(
                [
                    st.session_state.data,
                    pd.DataFrame([new_data])
                ],
                ignore_index=True
            )

            save_data(st.session_state.data)

            st.success("✅ SOS Alert Sent Successfully")
            st.toast("Emergency Alert Registered 🚨")

    st.divider()

    st.markdown("## 📡 Live Emergency Feed")

    c1, c2, c3 = st.columns(3)

    c1.success("🟢 Rescue Teams Active")
    c2.warning("🟡 Heavy Rain Expected")
    c3.error("🔴 High Risk Zone Detected")

    st.divider()

    st.markdown("## 📋 Your Emergency Requests")

    df = st.session_state.data

    if not df.empty:

        for _, row in df.iterrows():

            with st.container():

                st.markdown('<div class="card">', unsafe_allow_html=True)

                c1, c2 = st.columns([1, 2])

                with c1:
                    show_image(row)

                with c2:

                    st.subheader(f"🚨 {row['Type']}")

                    st.write(f"📍 District: {row['District']}")
                    st.write(f"👥 People: {row['People']}")
                    st.write(f"⚠️ Priority: {row['Priority']}")
                    st.write(f"📌 Status: {row['Status']}")
                    st.write(f"🕒 Time: {row['Time']}")

                    supplies = predict_supplies(
                        row["Type"],
                        row["People"],
                        row["Priority"]
                    )

                    st.markdown("### 🧠 AI Suggested Resources")

                    for item in supplies:
                        st.write(f"✅ {item}")

                st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("No SOS requests yet.")

# =========================
# ADMIN PANEL
# =========================
def admin_panel():

    df = st.session_state.data

    st.markdown("## 🛡️ AI Disaster Command Center")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🚨 Total SOS", len(df))

    c2.metric(
        "🟡 Pending",
        len(df[df["Status"] == "Pending"])
    )

    c3.metric(
        "👥 People Affected",
        int(pd.to_numeric(df["People"], errors="coerce").fillna(0).sum())
    )

    c4.metric(
        "⚠️ Risk Level",
        risk_level(df)
    )

    st.divider()

    st.markdown("""
    <div class="card">
    <h3>🧠 AI Situation Report</h3>
    <ul>
    <li>Urban areas showing high SOS density</li>
    <li>Flood risk increasing due to rainfall</li>
    <li>Emergency response optimization recommended</li>
    <li>AI monitoring active 24/7</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🗺️ Live Disaster Map")

    st.plotly_chart(
        build_map(df),
        use_container_width=True
    )

    st.divider()

    st.markdown("## 📊 Disaster Analytics")

    if not df.empty:

        type_counts = df["Type"].value_counts()

        c1, c2 = st.columns(2)

        with c1:
            st.bar_chart(type_counts)

        with c2:

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=type_counts.index,
                        values=type_counts.values,
                        hole=0.4
                    )
                ]
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.divider()

    # =========================
    # AI RESOURCE DASHBOARD
    # =========================
    st.markdown("## 🧠 AI Resource Supply Dashboard")

    if not df.empty:

        all_supplies = []

        for _, row in df.iterrows():

            supplies = predict_supplies(
                row["Type"],
                row["People"],
                row["Priority"]
            )

            all_supplies.extend(supplies)

        supply_df = pd.DataFrame(
            all_supplies,
            columns=["Resources"]
        )

        supply_counts = supply_df["Resources"].value_counts()

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("### 🚑 Required Resources")

            st.dataframe(
                supply_counts,
                use_container_width=True
            )

        with c2:

            fig = go.Figure(
                data=[
                    go.Bar(
                        x=supply_counts.index,
                        y=supply_counts.values
                    )
                ]
            )

            fig.update_layout(
                title="Emergency Resource Demand",
                xaxis_title="Resources",
                yaxis_title="Count",
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.divider()

    st.markdown("## 🚨 Emergency Queue")

    if not df.empty:

        for _, row in df.iterrows():

            st.markdown('<div class="card">', unsafe_allow_html=True)

            c1, c2 = st.columns([1, 2])

            with c1:
                show_image(row)

            with c2:

                st.subheader(f"🚨 {row['Type']}")

                st.write(f"📍 District: {row['District']}")
                st.write(f"👥 People: {row['People']}")
                st.write(f"⚠️ Priority: {row['Priority']}")
                st.write(f"📌 Status: {row['Status']}")
                st.write(f"🕒 Time: {row['Time']}")

                supplies = predict_supplies(
                    row["Type"],
                    row["People"],
                    row["Priority"]
                )

                st.markdown("### 🧠 Required Emergency Resources")

                for item in supplies:
                    st.write(f"🚑 {item}")

            st.markdown('</div>', unsafe_allow_html=True)

    if not df.empty:

        st.markdown("## ⚙️ Update Emergency Status")

        selected_id = st.selectbox(
            "Select SOS ID",
            df["ID"].tolist()
        )

        new_status = st.selectbox(
            "Update Status",
            ["Pending", "In Progress", "Resolved"]
        )

        if st.button("✅ UPDATE STATUS"):

            st.session_state.data.loc[
                st.session_state.data["ID"] == selected_id,
                "Status"
            ] = new_status

            save_data(st.session_state.data)

            st.success("Status Updated Successfully")

# =========================
# LOGIN SYSTEM
# =========================
if "role" not in st.session_state:

    st.markdown("""
    <div class="card">
    <h2>🚨 Secure Access Portal</h2>
    <p>Government Emergency Intelligence System</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:

        st.image(
            "https://images.unsplash.com/photo-1604275689235-fdc521556c16?q=80&w=1170&auto=format&fit=crop",
            use_container_width=True
        )

        st.image(
            "https://plus.unsplash.com/premium_photo-1695914233513-6f9ca230abdb?w=1000&auto=format&fit=crop&q=60",
            use_container_width=True
        )

    with col2:

        name = st.text_input("👤 Enter Name")

        role = st.selectbox(
            "🔐 Select Role",
            ["User", "Admin"]
        )

        if st.button("🚀 ENTER SYSTEM"):

            st.session_state.role = role.lower()
            st.session_state.username = name

            st.rerun()

else:

    st.sidebar.title("🚨 Dashboard")

    st.sidebar.success(
        f"Logged in: {st.session_state.username}"
    )

    st.sidebar.write(
        f"Role: {st.session_state.role}"
    )

    st.sidebar.info("""
🛰️ AI Monitoring Active
📡 Satellite Connected
🚒 Emergency Network Online
""")

    if st.sidebar.button("Logout"):

        st.session_state.clear()
        st.rerun()

    if st.session_state.role == "user":
        user_panel()

    else:
        admin_panel()