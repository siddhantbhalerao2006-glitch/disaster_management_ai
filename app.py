import streamlit as st
import pandas as pd
from datetime import datetime
import random
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# CONFIG & SETTINGS
# ─────────────────────────────────────────────
st.set_page_config(page_title="DisasterNet Command", page_icon="🚨", layout="wide")

# District Coordinates for Mapping
DISTRICT_MAP = {
    "Kothrud": {"lat": 18.5074, "lon": 73.8077},
    "Hadapsar": {"lat": 18.5089, "lon": 73.9259},
    "Pune North": {"lat": 18.5538, "lon": 73.8531},
    "Wakad": {"lat": 18.5987, "lon": 73.7607},
    "Baner": {"lat": 18.5590, "lon": 73.7787},
    "Aundh": {"lat": 18.5580, "lon": 73.8075},
    "Hinjewadi": {"lat": 18.5913, "lon": 73.7389}
}

# CSS Styling
st.markdown("""
<style>
    .main {background-color: #0b0c10;}
    .stApp {background-color: #0b0c10; color: #c5c6c7;}
    .metric-card {
        background: rgba(102, 252, 241, 0.05);
        padding: 20px; border-radius: 15px; border: 1px solid #45a29e;
        text-align: center;
    }
    h1, h2, h3 {color: #66fcf1 !important;}
    .stNotification { border-radius: 10px; border-left: 5px solid #66fcf1; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────
if "pending_requests" not in st.session_state:
    # Pre-seeding some data for the graphs
    initial_data = []
    for i in range(1, 15):
        dist = random.choice(list(DISTRICT_MAP.keys()))
        initial_data.append({
            "ID": f"SOS-{1000+i}", "Name": f"Resident {i}", "District": dist,
            "People": random.randint(1, 8), "Type": random.choice(["Medical", "Food", "Rescue"]),
            "Priority": random.choice(["High", "Medium", "Low"]), "Status": "Dispatched",
            "lat": DISTRICT_MAP[dist]["lat"], "lon": DISTRICT_MAP[dist]["lon"]
        })
    st.session_state.pending_requests = pd.DataFrame(initial_data)

if "role" not in st.session_state: st.session_state.role = None

# ─────────────────────────────────────────────
# USER VIEW
# ─────────────────────────────────────────────
def user_view():
    st.title(f"🆘 Emergency Terminal: {st.session_state.username}")
    
    # SOS Notification Area
    my_requests = st.session_state.pending_requests[st.session_state.pending_requests["Name"] == st.session_state.username]
    if not my_requests.empty:
        latest_status = my_requests.iloc[-1]["Status"]
        if latest_status == "Dispatched":
            st.success(f"🔔 **Notification:** Help is on the way! Your request {my_requests.iloc[-1]['ID']} has been dispatched.")
        elif latest_status == "In Progress":
            st.info(f"🔔 **Notification:** Rescue team is currently processing your request.")
    
    tab1, tab2 = st.tabs(["🚀 SOS Broadcast", "👤 My Profile"])

    with tab1:
        col_form, col_map = st.columns([2, 3])
        with col_form:
            st.markdown("### Send Emergency Signal")
            with st.form("user_sos"):
                dist = st.selectbox("Current District", list(DISTRICT_MAP.keys()))
                ppl = st.number_input("People Affected", 1, 50)
                need = st.selectbox("Service", ["Rescue", "Medical Aid", "Supplies"])
                prio = st.select_slider("Urgency", ["Low", "Medium", "High"], "Medium")
                if st.form_submit_button("ACTIVATE SOS", type="primary"):
                    new_id = f"SOS-{random.randint(2000, 9999)}"
                    new_entry = pd.DataFrame([{
                        "ID": new_id, "Name": st.session_state.username, "District": dist,
                        "People": ppl, "Type": need, "Priority": prio, "Status": "Pending",
                        "lat": DISTRICT_MAP[dist]["lat"], "lon": DISTRICT_MAP[dist]["lon"]
                    }])
                    st.session_state.pending_requests = pd.concat([st.session_state.pending_requests, new_entry], ignore_index=True)
                    st.toast("SOS Broadcasted!")
        
        with col_map:
            st.markdown("### Regional SOS Map")
            fig = px.scatter_mapbox(st.session_state.pending_requests, lat="lat", lon="lon", color="Priority", 
                                    size="People", hover_name="Type", zoom=10, height=400)
            fig.update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### Manage Personal Records")
        st.text_input("Emergency Contact Number", "+91 ")
        st.selectbox("Blood Group", ["O+", "A+", "B+", "AB+", "O-", "A-", "B-", "AB-"])
        st.button("Update Records")

# ─────────────────────────────────────────────
# ADMIN VIEW
# ─────────────────────────────────────────────
def admin_dashboard():
    st.title("🛡️ Command Center Analytics")
    df = st.session_state.pending_requests
    
    # Row 1: Key Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="metric-card"><h3>{len(df)}</h3><p>Total SOS</p></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-card"><h3>{len(df[df["Status"]=="Pending"])}</h3><p>Unattended</p></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-card"><h3>{int(df["People"].sum())}</h3><p>Souls At Risk</p></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="metric-card"><h3>{df["District"].mode()[0] if not df.empty else "N/A"}</h3><p>Hotspot</p></div>', unsafe_allow_html=True)
    
    st.divider()

    # Row 2: Graphs
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("### Incident Distribution")
        fig_bar = px.bar(df, x="District", color="Priority", title="SOS Counts by Area", barmode="group", template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with g2:
        st.markdown("### Rescue Progress")
        status_count = df["Status"].value_counts().reset_index()
        fig_pie = px.pie(status_count, values='count', names='Status', hole=0.4, template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("### 📋 Live Operational Log")
    edited_df = st.data_editor(df, use_container_width=True, hide_index=True)
    if st.button("💾 Sync Updates"):
        st.session_state.pending_requests = edited_df
        st.success("Operational log synced with field units.")

# ─────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚨 AI disaster management system
    ")
    if st.session_state.role is None:
        user_input = st.text_input("User Name")
        role_input = st.selectbox("Terminal Access", ["Citizen", "Admin"])
        if st.button("Authenticate"):
            st.session_state.role = role_input.lower()
            st.session_state.username = user_input or "Citizen_Alpha"
            st.rerun()
    else:
        st.write(f"Logged in: {st.session_state.username}")
        if st.button("Disconnect"):
            st.session_state.role = None
            st.rerun()

if st.session_state.role == "admin": admin_dashboard()
elif st.session_state.role == "citizen": user_view()
else: st.info("Please login to access the Relief Command Terminal.")
