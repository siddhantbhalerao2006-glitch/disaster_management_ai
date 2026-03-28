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
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap');

/* ── BASE ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #080c17;
    color: #e2e5f0;
}
.main .block-container { padding: 1.6rem 2rem 3rem; max-width: 1300px; }
h1,h2,h3,h4 { font-family:'Syne',sans-serif; letter-spacing:-0.02em; }

/* ── TOP HEADER BAR ── */
.top-bar {
    display:flex; justify-content:space-between; align-items:flex-end;
    margin-bottom:1.4rem; padding-bottom:1rem;
    border-bottom:1px solid #1a2035;
}
.top-bar-title  { font-family:'Syne',sans-serif; font-weight:800; font-size:1.75rem; letter-spacing:-0.03em; }
.top-bar-title span { color:#f97316; }
.top-bar-meta   { font-size:0.78rem; color:#5a637a; letter-spacing:0.04em; }
.top-bar-right  { text-align:right; }
.live-badge {
    display:inline-flex; align-items:center; gap:6px;
    font-size:0.72rem; font-weight:600; letter-spacing:0.08em; text-transform:uppercase;
    background:#0f2010; border:1px solid #166534; color:#4ade80;
    padding:4px 12px; border-radius:20px;
}
.live-dot { width:7px; height:7px; border-radius:50%; background:#4ade80;
            animation:blink 1.4s ease-in-out infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

/* ── SUMMARY STAT CARDS ── */
.summary-row { display:flex; gap:0.9rem; margin-bottom:1.5rem; flex-wrap:wrap; }
.summary-card {
    flex:1; min-width:130px;
    background:#101726; border:1px solid #1a2642;
    border-radius:13px; padding:1rem 1.2rem;
    position:relative; overflow:hidden;
}
.summary-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    background: var(--accent);
}
.s-num  { font-family:'Syne',sans-serif; font-size:1.9rem; font-weight:800; line-height:1; color:var(--accent); }
.s-lbl  { font-size:0.7rem; letter-spacing:0.07em; text-transform:uppercase; color:#4a5270; margin-top:5px; }
.s-sub  { font-size:0.78rem; color:#6b7591; margin-top:3px; }

/* ── STOCK SECTION ── */
.section-hdr {
    font-family:'Syne',sans-serif; font-weight:700; font-size:1.1rem;
    margin-bottom:0.9rem; padding-bottom:0.5rem;
    border-bottom:1px solid #1a2035; display:flex; align-items:center; gap:0.5rem;
}
.stock-card {
    background:#101726; border:1px solid #1a2642;
    border-radius:13px; padding:1.1rem 1.3rem; margin-bottom:0.75rem;
    transition:border-color 0.2s;
}
.stock-card:hover { border-color:#2a3a5a; }
.stock-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem; }
.stock-name   { font-family:'Syne',sans-serif; font-weight:700; font-size:0.95rem; display:flex; align-items:center; gap:0.4rem; }
.stock-nums   { font-size:0.82rem; color:#6b7591; }
.stock-nums strong { color:#e2e5f0; }
.pct-badge {
    font-size:0.72rem; font-weight:700; letter-spacing:0.06em;
    padding:3px 9px; border-radius:20px; text-transform:uppercase;
}
.badge-ok   { background:#0f2a10; color:#4ade80; border:1px solid #16612444; }
.badge-low  { background:#2d1f05; color:#fbbf24; border:1px solid #92400e44; }
.badge-crit { background:#2a0a0a; color:#f87171; border:1px solid #7f1d1d44; }

/* progress bar override */
.stProgress > div > div > div > div { border-radius:4px !important; }

/* ── REQUEST TABLE ── */
.req-table-wrap {
    background:#101726; border:1px solid #1a2642;
    border-radius:13px; overflow:hidden; margin-bottom:1.2rem;
}
.req-table-head {
    display:grid;
    grid-template-columns: 110px 1fr 1fr 120px 130px;
    background:#0d1422; padding:0.65rem 1.1rem;
    border-bottom:1px solid #1a2642;
    font-size:0.68rem; letter-spacing:0.09em; text-transform:uppercase; color:#4a5270; font-weight:600;
}
.req-row {
    display:grid;
    grid-template-columns: 110px 1fr 1fr 120px 130px;
    padding:0.75rem 1.1rem;
    border-bottom:1px solid #111928;
    align-items:center; font-size:0.85rem;
    transition:background 0.15s;
}
.req-row:last-child { border-bottom:none; }
.req-row:hover { background:#0d1932; }
.req-id     { font-family:'Syne',sans-serif; font-weight:700; color:#f97316; }
.req-dist   { color:#c8cfe0; }
.req-res    { color:#9aa3bf; font-size:0.8rem; }
.status-pill {
    display:inline-block; font-size:0.68rem; font-weight:700;
    letter-spacing:0.07em; text-transform:uppercase;
    padding:3px 10px; border-radius:20px;
}
.pill-pending    { background:#1a1405; color:#fbbf24; border:1px solid #92400e66; }
.pill-dispatched { background:#0a1a2a; color:#60a5fa; border:1px solid #1d4ed866; }
.pill-delivered  { background:#0a1f0c; color:#4ade80; border:1px solid #16613466; }

/* ── BUTTONS ── */
.stButton > button {
    font-family:'Syne',sans-serif; font-weight:700;
    font-size:0.78rem; letter-spacing:0.04em;
    border-radius:8px; padding:0.38rem 1rem;
    transition:all 0.18s; border:none;
}
.stButton > button[kind="primary"],
.stButton > button:not([kind]) {
    background:linear-gradient(135deg,#f97316,#ea580c);
    color:#fff;
}
.stButton > button:hover { opacity:0.82; transform:translateY(-1px); }

/* ── DISPATCH MODAL AREA ── */
.dispatch-panel {
    background:#101726; border:1px solid #1a2642;
    border-left:4px solid #f97316;
    border-radius:13px; padding:1.3rem 1.5rem; margin-top:1rem;
}
.dispatch-panel-title {
    font-family:'Syne',sans-serif; font-weight:700; font-size:1rem;
    color:#f97316; margin-bottom:0.9rem;
}

/* ── INPUTS ── */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea textarea {
    background:#0a1020 !important; border:1px solid #1a2642 !important;
    border-radius:9px !important; color:#e2e5f0 !important;
    font-family:'DM Sans',sans-serif !important;
}
.stSelectbox label,.stTextInput label,.stNumberInput label,.stTextArea label,.stRadio label {
    font-size:0.72rem !important; letter-spacing:0.06em !important;
    text-transform:uppercase !important; color:#4a5270 !important; font-weight:500 !important;
}

/* ── ALERTS ── */
.stSuccess, .stError, .stWarning, .stInfo { border-radius:10px !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background:#0a0f1c; border-right:1px solid #1a2035;
}
section[data-testid="stSidebar"] .block-container { padding:1.5rem 1rem; }
.sb-title { font-family:'Syne',sans-serif; font-weight:800; font-size:1.2rem; color:#f97316; margin-bottom:0.3rem; }
.sb-sub   { font-size:0.72rem; color:#4a5270; letter-spacing:0.05em; margin-bottom:1.4rem; }
.sb-metric { background:#101726; border:1px solid #1a2642; border-radius:10px; padding:0.7rem 1rem; margin-bottom:0.6rem; }
.sb-metric-val { font-family:'Syne',sans-serif; font-weight:700; font-size:1.3rem; }
.sb-metric-lbl { font-size:0.68rem; text-transform:uppercase; letter-spacing:0.07em; color:#4a5270; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "requests" not in st.session_state:
    st.session_state.requests = [
        {"id":"REQ-001","district":"Patna North",    "resources":"Water ×200L, Food ×50 pkts",        "status":"Pending",    "priority":"High",   "submitted":"09:12"},
        {"id":"REQ-002","district":"Guwahati East",  "resources":"Medical Kits ×15, Tents ×8",         "status":"Dispatched", "priority":"Critical","submitted":"09:34"},
        {"id":"REQ-003","district":"Bhubaneswar",    "resources":"Water ×500L, Tents ×20",             "status":"Pending",    "priority":"Critical","submitted":"10:01"},
        {"id":"REQ-004","district":"Visakhapatnam",  "resources":"Food ×120 pkts, Medical Kits ×30",   "status":"Pending",    "priority":"High",   "submitted":"10:18"},
        {"id":"REQ-005","district":"Kolkata South",  "resources":"Tents ×40, Water ×300L",             "status":"Delivered",  "priority":"Moderate","submitted":"08:45"},
        {"id":"REQ-006","district":"Varanasi",       "resources":"Medical Kits ×25, Food ×80 pkts",    "status":"Pending",    "priority":"High",   "submitted":"10:52"},
        {"id":"REQ-007","district":"Surat Coastal",  "resources":"Water ×1000L, Tents ×35",            "status":"Dispatched", "priority":"Critical","submitted":"11:05"},
        {"id":"REQ-008","district":"Puri",           "resources":"Food ×60 pkts, Medical Kits ×10",    "status":"Pending",    "priority":"Moderate","submitted":"11:22"},
    ]

if "stock" not in st.session_state:
    st.session_state.stock = {
        "Water":   {"current":18400, "capacity":25000, "unit":"Litres",  "icon":"💧", "reserve":5000},
        "Food":    {"current":3200,  "capacity":6000,  "unit":"Packets", "icon":"🍱", "reserve":500},
        "Medical": {"current":280,   "capacity":500,   "unit":"Kits",    "icon":"🩺", "reserve":50},
        "Tents":   {"current":620,   "capacity":1000,  "unit":"Units",   "icon":"⛺", "reserve":100},
    }

if "dispatch_target" not in st.session_state:
    st.session_state.dispatch_target = None

if "toast_msg" not in st.session_state:
    st.session_state.toast_msg = None

if "activity_log" not in st.session_state:
    st.session_state.activity_log = [
        {"time":"08:45","action":"REQ-005 marked Delivered","user":"Mgr. Kapoor"},
        {"time":"09:34","action":"REQ-002 dispatched","user":"Mgr. Kapoor"},
        {"time":"11:05","action":"REQ-007 dispatched","user":"Mgr. Kapoor"},
    ]

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-title">📦 DisasterNet</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">WAREHOUSE COMMAND CENTRE</div>', unsafe_allow_html=True)

    reqs = st.session_state.requests
    pending_count    = sum(1 for r in reqs if r["status"]=="Pending")
    dispatched_count = sum(1 for r in reqs if r["status"]=="Dispatched")
    delivered_count  = sum(1 for r in reqs if r["status"]=="Delivered")

    st.markdown(f'<div class="sb-metric"><div class="sb-metric-val" style="color:#fbbf24">{pending_count}</div><div class="sb-metric-lbl">Pending Requests</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sb-metric"><div class="sb-metric-val" style="color:#60a5fa">{dispatched_count}</div><div class="sb-metric-lbl">In Transit</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sb-metric"><div class="sb-metric-val" style="color:#4ade80">{delivered_count}</div><div class="sb-metric-lbl">Delivered</div></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("**🕐 Activity Log**")
    for entry in reversed(st.session_state.activity_log[-6:]):
        st.markdown(f"<small style='color:#4a5270'>{entry['time']}</small><br><small>{entry['action']}</small>", unsafe_allow_html=True)
        st.markdown("")

    st.divider()
    st.markdown(f"<small style='color:#4a5270'>🗓 {datetime.now().strftime('%d %b %Y, %H:%M')}<br>Logged in as: <b>Mgr. Anil Kapoor</b></small>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TOP HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="top-bar">
    <div>
        <div class="top-bar-title">📦 <span>Warehouse</span> Manager Dashboard</div>
        <div class="top-bar-meta">PATNA CENTRAL RELIEF HUB &nbsp;·&nbsp; BIHAR ZONE &nbsp;·&nbsp; {datetime.now().strftime('%d %B %Y')}</div>
    </div>
    <div class="top-bar-right">
        <div class="live-badge"><div class="live-dot"></div> Live</div>
        <div class="top-bar-meta" style="margin-top:6px">Auto-refresh every 30s</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SUMMARY STAT CARDS
# ─────────────────────────────────────────────
reqs   = st.session_state.requests
stock  = st.session_state.stock

critical_pending = sum(1 for r in reqs if r["status"]=="Pending" and r["priority"]=="Critical")
low_stock_items  = sum(1 for s in stock.values() if s["current"]/s["capacity"] < 0.35)

st.markdown(f"""
<div class="summary-row">
    <div class="summary-card" style="--accent:#fbbf24">
        <div class="s-num">{pending_count}</div>
        <div class="s-lbl">Pending Requests</div>
        <div class="s-sub">{critical_pending} critical priority</div>
    </div>
    <div class="summary-card" style="--accent:#60a5fa">
        <div class="s-num">{dispatched_count}</div>
        <div class="s-lbl">In Transit</div>
        <div class="s-sub">Vehicles on route</div>
    </div>
    <div class="summary-card" style="--accent:#4ade80">
        <div class="s-num">{delivered_count}</div>
        <div class="s-lbl">Delivered Today</div>
        <div class="s-sub">Completed successfully</div>
    </div>
    <div class="summary-card" style="--accent:#f97316">
        <div class="s-num">{low_stock_items}</div>
        <div class="s-lbl">Low Stock Alerts</div>
        <div class="s-sub">Below 35% capacity</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TOAST / SUCCESS MESSAGE
# ─────────────────────────────────────────────
if st.session_state.toast_msg:
    st.success(st.session_state.toast_msg)
    st.session_state.toast_msg = None

# ─────────────────────────────────────────────
# MAIN LAYOUT: Stock (left) | Requests (right)
# ─────────────────────────────────────────────
left_col, right_col = st.columns([1, 1.65], gap="large")

# ══════════════════════════════
# LEFT: STOCK PROGRESS BARS
# ══════════════════════════════
with left_col:
    st.markdown('<div class="section-hdr">🗄️ Stock Inventory</div>', unsafe_allow_html=True)

    for name, data in stock.items():
        pct  = data["current"] / data["capacity"]
        used = data["current"]
        cap  = data["capacity"]
        unit = data["unit"]
        icon = data["icon"]
        res  = data["reserve"]

        if pct > 0.5:
            bar_color  = "#22c55e"
            badge_cls  = "badge-ok"
            badge_text = f"{pct*100:.0f}% OK"
        elif pct > 0.3:
            bar_color  = "#f59e0b"
            badge_cls  = "badge-low"
            badge_text = f"{pct*100:.0f}% LOW"
        else:
            bar_color  = "#ef4444"
            badge_cls  = "badge-crit"
            badge_text = f"{pct*100:.0f}% CRITICAL"

        st.markdown(f"""
        <div class="stock-card">
            <div class="stock-header">
                <div class="stock-name">{icon} {name}</div>
                <span class="pct-badge {badge_cls}">{badge_text}</span>
            </div>
            <div class="stock-nums" style="margin-bottom:8px">
                <strong>{used:,}</strong> / {cap:,} {unit}
                &nbsp;·&nbsp; Reserve: {res:,} {unit}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Inject color via CSS override per bar
        st.markdown(f"""
        <style>
        div[data-testid="stProgress"]:last-of-type > div > div > div > div {{
            background: {bar_color} !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        st.progress(pct)

    # ── Restock Form ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-hdr">➕ Restock Item</div>', unsafe_allow_html=True)
    with st.expander("Open Restock Panel", expanded=False):
        rs_item = st.selectbox("Item", list(stock.keys()), key="rs_item")
        rs_qty  = st.number_input("Quantity to Add", min_value=1, max_value=50000, value=100, key="rs_qty")
        if st.button("Confirm Restock", key="restock_btn"):
            old = st.session_state.stock[rs_item]["current"]
            cap = st.session_state.stock[rs_item]["capacity"]
            new = min(old + rs_qty, cap)
            st.session_state.stock[rs_item]["current"] = new
            st.session_state.activity_log.append({
                "time": datetime.now().strftime("%H:%M"),
                "action": f"Restocked {rs_item} +{rs_qty} {st.session_state.stock[rs_item]['unit']}",
                "user": "Mgr. Kapoor"
            })
            st.session_state.toast_msg = f"✅ Restocked {rs_item} by {rs_qty:,} {st.session_state.stock[rs_item]['unit']}. New total: {new:,}."
            st.rerun()

# ══════════════════════════════
# RIGHT: DISPATCH REQUESTS TABLE
# ══════════════════════════════
with right_col:
    st.markdown('<div class="section-hdr">📬 Dispatch Requests</div>', unsafe_allow_html=True)

    # Filter toolbar
    fcol1, fcol2, fcol3 = st.columns([1.2, 1.2, 1])
    with fcol1:
        filter_status = st.selectbox("Filter Status", ["All","Pending","Dispatched","Delivered"], key="filter_status")
    with fcol2:
        filter_priority = st.selectbox("Filter Priority", ["All","Critical","High","Moderate"], key="filter_priority")
    with fcol3:
        sort_by = st.selectbox("Sort By", ["Submitted","Priority","Status"], key="sort_by")

    # Apply filters
    display_reqs = list(st.session_state.requests)
    if filter_status   != "All": display_reqs = [r for r in display_reqs if r["status"]   == filter_status]
    if filter_priority != "All": display_reqs = [r for r in display_reqs if r["priority"] == filter_priority]
    priority_order = {"Critical":0,"High":1,"Moderate":2}
    if sort_by == "Priority":  display_reqs.sort(key=lambda r: priority_order.get(r["priority"],9))
    elif sort_by == "Status":  display_reqs.sort(key=lambda r: r["status"])

    # Table header
    st.markdown("""
    <div class="req-table-wrap">
        <div class="req-table-head">
            <div>Request ID</div><div>District</div><div>Resources Needed</div><div>Status</div><div>Action</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Table rows — rendered with st.columns for interactive buttons
    if not display_reqs:
        st.info("No requests match the current filters.")
    else:
        for req in display_reqs:
            status_cls = {
                "Pending":    "pill-pending",
                "Dispatched": "pill-dispatched",
                "Delivered":  "pill-delivered",
            }.get(req["status"], "pill-pending")

            priority_color = {
                "Critical": "#f87171",
                "High":     "#fb923c",
                "Moderate": "#fbbf24",
            }.get(req["priority"], "#e2e5f0")

            # Use columns: ID | District | Resources | Status | Action
            c1, c2, c3, c4, c5 = st.columns([0.9, 1.1, 1.6, 1.0, 1.1])

            with c1:
                st.markdown(f"<div style='font-family:Syne,sans-serif;font-weight:700;color:#f97316;padding-top:6px'>{req['id']}</div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div style='padding-top:6px;font-size:0.85rem'>{req['district']}<br><span style='font-size:0.72rem;color:{priority_color}'>{req['priority']}</span></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div style='padding-top:6px;font-size:0.8rem;color:#9aa3bf'>{req['resources']}</div>", unsafe_allow_html=True)
            with c4:
                st.markdown(f"<span class='status-pill {status_cls}'>{req['status']}</span>", unsafe_allow_html=True)
            with c5:
                if req["status"] == "Pending":
                    if st.button("🚚 Dispatch", key=f"dispatch_{req['id']}"):
                        st.session_state.dispatch_target = req["id"]
                        st.rerun()
                elif req["status"] == "Dispatched":
                    if st.button("✅ Delivered", key=f"deliver_{req['id']}"):
                        for r in st.session_state.requests:
                            if r["id"] == req["id"]:
                                r["status"] = "Delivered"
                        st.session_state.activity_log.append({
                            "time": datetime.now().strftime("%H:%M"),
                            "action": f"{req['id']} marked Delivered — {req['district']}",
                            "user": "Mgr. Kapoor"
                        })
                        st.session_state.toast_msg = f"📦 {req['id']} ({req['district']}) marked as Delivered!"
                        st.rerun()
                else:
                    st.markdown("<div style='padding-top:4px;font-size:0.78rem;color:#4a5270'>—</div>", unsafe_allow_html=True)

            st.markdown("<hr style='border-color:#111928;margin:4px 0'>", unsafe_allow_html=True)

    st.caption(f"Showing {len(display_reqs)} of {len(st.session_state.requests)} requests")

# ─────────────────────────────────────────────
# DISPATCH CONFIRMATION PANEL
# ─────────────────────────────────────────────
if st.session_state.dispatch_target:
    tid  = st.session_state.dispatch_target
    treq = next((r for r in st.session_state.requests if r["id"] == tid), None)

    if treq:
        st.markdown("---")
        st.markdown(f"""
        <div class="dispatch-panel">
            <div class="dispatch-panel-title">🚚 Confirm Dispatch — {tid}</div>
        </div>
        """, unsafe_allow_html=True)

        d1, d2, d3 = st.columns(3)
        with d1:
            vehicle  = st.selectbox("Vehicle Type",   ["Relief Truck","Ambulance","Cargo Van","Boat","Helicopter"], key="d_vehicle")
            driver   = st.text_input("Driver / Team Lead", placeholder="e.g. Ramesh Kumar", key="d_driver")
        with d2:
            eta      = st.selectbox("ETA",            ["15 min","30 min","45 min","1 hour","2 hours","3+ hours"], key="d_eta")
            contact  = st.text_input("Contact Number",placeholder="+91 9XXXXXXXXX", key="d_contact")
        with d3:
            route    = st.text_area("Route / Notes",  placeholder="NH-30 via Patna Bridge…", height=104, key="d_route")

        bc1, bc2, bc3 = st.columns([1, 1, 3])
        with bc1:
            if st.button("✅ Confirm Dispatch", key="confirm_dispatch"):
                if not driver:
                    st.error("Driver name is required before dispatching.")
                else:
                    for r in st.session_state.requests:
                        if r["id"] == tid:
                            r["status"] = "Dispatched"
                    st.session_state.activity_log.append({
                        "time": datetime.now().strftime("%H:%M"),
                        "action": f"{tid} dispatched via {vehicle} · Driver: {driver} · ETA {eta}",
                        "user": "Mgr. Kapoor"
                    })
                    st.session_state.toast_msg = f"🚚 {tid} dispatched! {vehicle} en route to {treq['district']} — ETA {eta}."
                    st.session_state.dispatch_target = None
                    st.rerun()
        with bc2:
            if st.button("✖ Cancel", key="cancel_dispatch"):
                st.session_state.dispatch_target = None
                st.rerun()
