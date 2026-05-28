import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DisasterNet — Warehouse Dashboard",
    page_icon="📦",
    layout="wide",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
html, body {
    background-color: #080c17;
    color: #e2e5f0;
    font-family: sans-serif;
}

.section-hdr {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 10px;
}

.summary-card {
    background:#101726;
    padding:15px;
    border-radius:12px;
    border:1px solid #1a2642;
}

.status-pill {
    padding:4px 10px;
    border-radius:20px;
    font-size:12px;
    font-weight:700;
}

.pending { background:#3a2b08; color:#fbbf24; }
.dispatch { background:#0a223a; color:#60a5fa; }
.delivered { background:#0c2c14; color:#4ade80; }

.stButton > button {
    background:linear-gradient(135deg,#f97316,#ea580c);
    color:white;
    border:none;
    border-radius:8px;
    font-weight:700;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "requests" not in st.session_state:
    st.session_state.requests = [
        {"id":"REQ-001","district":"Patna North","resources":"Water ×200L","status":"Pending","priority":"High"},
        {"id":"REQ-002","district":"Guwahati East","resources":"Medical Kits ×15","status":"Dispatched","priority":"Critical"},
        {"id":"REQ-003","district":"Bhubaneswar","resources":"Food ×80","status":"Pending","priority":"Critical"},
        {"id":"REQ-004","district":"Surat Coastal","resources":"Tents ×30","status":"Delivered","priority":"Moderate"},
    ]

if "stock" not in st.session_state:
    st.session_state.stock = {
        "Water": {"current":18000,"capacity":25000,"icon":"💧"},
        "Food": {"current":3200,"capacity":6000,"icon":"🍱"},
        "Medical": {"current":280,"capacity":500,"icon":"🩺"},
        "Tents": {"current":620,"capacity":1000,"icon":"⛺"},
    }

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("📦 DisasterNet Warehouse Dashboard")

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("📊 Status")

    pending = sum(1 for r in st.session_state.requests if r["status"]=="Pending")
    dispatch = sum(1 for r in st.session_state.requests if r["status"]=="Dispatched")
    delivered = sum(1 for r in st.session_state.requests if r["status"]=="Delivered")

    st.metric("Pending", pending)
    st.metric("In Transit", dispatch)
    st.metric("Delivered", delivered)

# ─────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────
left, right = st.columns(2)

# ─────────────────────────────────────────────
# STOCK
# ─────────────────────────────────────────────
with left:
    st.markdown("## 🗄 Stock Inventory")

    for item, data in st.session_state.stock.items():
        pct = data["current"] / data["capacity"]

        st.markdown(f"""
        <div class="summary-card">
            <b>{data['icon']} {item}</b><br>
            {data['current']} / {data['capacity']}
        </div>
        """, unsafe_allow_html=True)

        st.progress(pct)

# ─────────────────────────────────────────────
# REQUESTS (FIXED BUTTON LOGIC)
# ─────────────────────────────────────────────
with right:
    st.markdown("## 📬 Requests")

    for i, req in enumerate(st.session_state.requests):

        c1, c2, c3, c4, c5 = st.columns([1,1.2,1.4,1,1])

        with c1:
            st.write(req["id"])

        with c2:
            st.write(req["district"])

        with c3:
            st.write(req["resources"])

        with c4:
            if req["status"] == "Pending":
                st.markdown('<span class="status-pill pending">Pending</span>', unsafe_allow_html=True)
            elif req["status"] == "Dispatched":
                st.markdown('<span class="status-pill dispatch">Dispatched</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-pill delivered">Delivered</span>', unsafe_allow_html=True)

        with c5:
            if req["status"] == "Pending":
                if st.button("Dispatch", key=f"d{i}"):
                    st.session_state.requests[i]["status"] = "Dispatched"
                    st.rerun()

            elif req["status"] == "Dispatched":
                if st.button("Done", key=f"c{i}"):
                    st.session_state.requests[i]["status"] = "Delivered"
                    st.rerun()

        st.divider()