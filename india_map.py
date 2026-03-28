import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DisasterNet — India Live Map",
    page_icon="🗺️",
    layout="wide",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0b0f1a;
    color: #e8eaf2;
}
.main .block-container { padding: 1.8rem 2.2rem 3rem; }

h1, h2, h3 { font-family: 'Syne', sans-serif; letter-spacing: -0.02em; }

/* Stat cards */
.stat-row { display: flex; gap: 0.9rem; margin-bottom: 1.4rem; flex-wrap: wrap; }
.stat-box {
    flex: 1; min-width: 120px;
    background: #141928; border: 1px solid #1e2a45;
    border-radius: 12px; padding: 0.9rem 1.1rem; text-align: center;
}
.stat-num { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800; line-height: 1; }
.stat-lbl { font-size: 0.7rem; letter-spacing: 0.07em; text-transform: uppercase; opacity: 0.5; margin-top: 4px; }
.red    { color: #f87171; }
.orange { color: #fb923c; }
.green  { color: #34d399; }
.blue   { color: #60a5fa; }

/* Legend card */
.legend-card {
    background: #141928; border: 1px solid #1e2a45;
    border-radius: 12px; padding: 1.1rem 1.3rem; margin-bottom: 1rem;
}
.legend-item { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.55rem; font-size: 0.85rem; }
.dot { width: 13px; height: 13px; border-radius: 50%; flex-shrink: 0; }

/* Filter panel */
.filter-label {
    font-size: 0.72rem; letter-spacing: 0.07em; text-transform: uppercase;
    color: #8a90a8; font-weight: 500; margin-bottom: 0.3rem;
}

/* Stbutton */
.stButton > button {
    background: linear-gradient(135deg, #f97316, #ea580c);
    color: #fff; border: none; border-radius: 9px;
    font-family: 'Syne', sans-serif; font-weight: 700;
    font-size: 0.82rem; letter-spacing: 0.03em;
    padding: 0.5rem 1.2rem;
}
.stButton > button:hover { opacity: 0.85; }

/* Selected zone info */
.zone-info-card {
    background: #141928; border: 1px solid #1e2a45;
    border-left: 4px solid #f97316;
    border-radius: 12px; padding: 1.1rem 1.3rem; margin-top: 0.8rem;
}
.zone-info-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1rem; margin-bottom: 0.4rem; }
.zone-info-row   { font-size: 0.83rem; color: #b0b8d0; margin-bottom: 0.25rem; }
.zone-info-row span { color: #e8eaf2; font-weight: 500; }

/* Checkbox / multiselect */
.stCheckbox label, .stMultiSelect label, .stSelectbox label { color: #8a90a8 !important; font-size: 0.78rem !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ZONE DATA
# ─────────────────────────────────────────────
ZONES = [
    # ── FLOOD ZONES (red) ──
    {"district": "Patna",           "state": "Bihar",       "lat": 25.5941, "lon": 85.1376,  "type": "Flood",   "severity": "Critical", "population": 312000, "warehouse": "Patna Central Relief Hub",      "last_updated": "10 min ago"},
    {"district": "Guwahati",        "state": "Assam",       "lat": 26.1445, "lon": 91.7362,  "type": "Flood",   "severity": "High",     "population": 178000, "warehouse": "Guwahati NE Depot",             "last_updated": "25 min ago"},
    {"district": "Varanasi",        "state": "Uttar Pradesh","lat": 25.3176, "lon": 82.9739, "type": "Flood",   "severity": "High",     "population": 245000, "warehouse": "Varanasi District Store",       "last_updated": "1 hr ago"},
    {"district": "Kolkata North",   "state": "West Bengal", "lat": 22.6761, "lon": 88.3615,  "type": "Flood",   "severity": "Moderate", "population": 420000, "warehouse": "Kolkata Port Relief Centre",    "last_updated": "40 min ago"},
    {"district": "Bhubaneswar",     "state": "Odisha",      "lat": 20.2961, "lon": 85.8245,  "type": "Flood",   "severity": "Critical", "population": 198000, "warehouse": "Bhubaneswar State Warehouse",   "last_updated": "5 min ago"},
    {"district": "Surat",           "state": "Gujarat",     "lat": 21.1702, "lon": 72.8311,  "type": "Flood",   "severity": "High",     "population": 310000, "warehouse": "Surat Industrial Relief Depot", "last_updated": "2 hrs ago"},

    # ── CYCLONE ZONES (orange) ──
    {"district": "Visakhapatnam",   "state": "Andhra Pradesh","lat": 17.6868,"lon": 83.2185, "type": "Cyclone", "severity": "Critical", "population": 287000, "warehouse": "Vizag Port Authority Store",    "last_updated": "8 min ago"},
    {"district": "Chennai Coast",   "state": "Tamil Nadu",  "lat": 13.0827, "lon": 80.2707,  "type": "Cyclone", "severity": "High",     "population": 510000, "warehouse": "Chennai Marina Depot",          "last_updated": "30 min ago"},
    {"district": "Puri",            "state": "Odisha",      "lat": 19.8135, "lon": 85.8312,  "type": "Cyclone", "severity": "High",     "population": 156000, "warehouse": "Puri Coastal Warehouse",        "last_updated": "15 min ago"},
    {"district": "Mangaluru",       "state": "Karnataka",   "lat": 12.9141, "lon": 74.8560,  "type": "Cyclone", "severity": "Moderate", "population": 134000, "warehouse": "Mangaluru Port Relief Hub",     "last_updated": "1 hr ago"},
    {"district": "Thiruvananthapuram","state": "Kerala",    "lat":  8.5241, "lon": 76.9366,  "type": "Cyclone", "severity": "Moderate", "population": 192000, "warehouse": "Trivandrum South Depot",        "last_updated": "45 min ago"},

    # ── SAFE ZONES (green) ──
    {"district": "Jaipur",          "state": "Rajasthan",   "lat": 26.9124, "lon": 75.7873,  "type": "Safe",    "severity": "None",     "population": 380000, "warehouse": "Jaipur Central Supply Base",    "last_updated": "2 hrs ago"},
    {"district": "Bengaluru",       "state": "Karnataka",   "lat": 12.9716, "lon": 77.5946,  "type": "Safe",    "severity": "None",     "population": 720000, "warehouse": "Bengaluru Metro Relief Hub",    "last_updated": "3 hrs ago"},
    {"district": "Pune",            "state": "Maharashtra", "lat": 18.5204, "lon": 73.8567,  "type": "Safe",    "severity": "None",     "population": 540000, "warehouse": "Pune Hadapsar Depot",           "last_updated": "1 hr ago"},
    {"district": "Hyderabad",       "state": "Telangana",   "lat": 17.3850, "lon": 78.4867,  "type": "Safe",    "severity": "None",     "population": 680000, "warehouse": "Hyderabad NDRF Base",           "last_updated": "2 hrs ago"},
    {"district": "Lucknow",         "state": "Uttar Pradesh","lat": 26.8467,"lon": 80.9462,  "type": "Safe",    "severity": "None",     "population": 290000, "warehouse": "Lucknow State Stockpile",       "last_updated": "4 hrs ago"},
    {"district": "Indore",          "state": "Madhya Pradesh","lat": 22.7196,"lon": 75.8577, "type": "Safe",    "severity": "None",     "population": 220000, "warehouse": "Indore Central Depot",          "last_updated": "3 hrs ago"},
]

df = pd.DataFrame(ZONES)

# ─────────────────────────────────────────────
# MARKER STYLES
# ─────────────────────────────────────────────
TYPE_STYLE = {
    "Flood":   {"color": "#ef4444", "icon": "tint",       "prefix": "fa", "dot": "#ef4444", "label": "🌊 Flood Zone"},
    "Cyclone": {"color": "#f97316", "icon": "warning",    "prefix": "fa", "dot": "#f97316", "label": "🌀 Cyclone Warning"},
    "Safe":    {"color": "#22c55e", "icon": "check",      "prefix": "fa", "dot": "#22c55e", "label": "✅ Safe Zone"},
}

SEV_BADGE = {
    "Critical": "<span style='background:#7f1d1d;color:#f87171;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700'>CRITICAL</span>",
    "High":     "<span style='background:#7c2d12;color:#fb923c;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700'>HIGH</span>",
    "Moderate": "<span style='background:#713f12;color:#fbbf24;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700'>MODERATE</span>",
    "None":     "<span style='background:#14532d;color:#4ade80;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700'>SAFE</span>",
}

def make_popup_html(row):
    sty  = TYPE_STYLE[row["type"]]
    badge = SEV_BADGE.get(row["severity"], "")
    pop_bg = {"Flood": "#1a0505", "Cyclone": "#1a0a00", "Safe": "#001a08"}[row["type"]]
    accent = sty["color"]
    return f"""
    <div style="font-family:'Segoe UI',sans-serif;width:230px;background:{pop_bg};
                border:1px solid {accent}55;border-radius:10px;padding:12px 14px;color:#e8eaf2">
        <div style="font-size:14px;font-weight:800;color:{accent};margin-bottom:6px;letter-spacing:-0.01em">
            {row['district']} {badge}
        </div>
        <div style="font-size:11px;color:#9ca3af;margin-bottom:8px">{row['state']}</div>
        <table style="width:100%;font-size:12px;border-collapse:collapse">
            <tr><td style="color:#6b7280;padding:2px 0">Disaster Type</td>
                <td style="text-align:right;color:{accent};font-weight:600">{row['type']}</td></tr>
            <tr><td style="color:#6b7280;padding:2px 0">Affected Pop.</td>
                <td style="text-align:right;font-weight:600">{row['population']:,}</td></tr>
            <tr><td style="color:#6b7280;padding:2px 0">Nearest Warehouse</td>
                <td style="text-align:right;color:#93c5fd;font-size:11px">{row['warehouse']}</td></tr>
            <tr><td style="color:#6b7280;padding:2px 0">Updated</td>
                <td style="text-align:right;color:#6b7280">{row['last_updated']}</td></tr>
        </table>
    </div>
    """

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:1.2rem">
    <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.9rem;letter-spacing:-0.03em">
        🗺️ <span style="color:#f97316">Disaster</span>Net — India Live Map
    </div>
    <div style="font-size:0.82rem;color:#8a90a8;letter-spacing:0.04em">
        REAL-TIME DISASTER ZONE MONITORING &nbsp;·&nbsp; INDIA
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STAT TILES
# ─────────────────────────────────────────────
flood_zones   = df[df["type"]=="Flood"]
cyclone_zones = df[df["type"]=="Cyclone"]
safe_zones    = df[df["type"]=="Safe"]
total_affected = df[df["type"]!="Safe"]["population"].sum()

st.markdown(f"""
<div class="stat-row">
    <div class="stat-box"><div class="stat-num red">{len(flood_zones)}</div><div class="stat-lbl">Flood Zones</div></div>
    <div class="stat-box"><div class="stat-num orange">{len(cyclone_zones)}</div><div class="stat-lbl">Cyclone Zones</div></div>
    <div class="stat-box"><div class="stat-num green">{len(safe_zones)}</div><div class="stat-lbl">Safe Zones</div></div>
    <div class="stat-box"><div class="stat-num blue">{total_affected:,}</div><div class="stat-lbl">People Affected</div></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LAYOUT: map + side panel
# ─────────────────────────────────────────────
map_col, panel_col = st.columns([3, 1])

with panel_col:
    # Legend
    st.markdown("""
    <div class="legend-card">
        <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:0.9rem;margin-bottom:0.8rem">Map Legend</div>
        <div class="legend-item"><div class="dot" style="background:#ef4444"></div> Flood Zone</div>
        <div class="legend-item"><div class="dot" style="background:#f97316"></div> Cyclone Warning</div>
        <div class="legend-item"><div class="dot" style="background:#22c55e"></div> Safe Zone</div>
    </div>
    """, unsafe_allow_html=True)

    # Filters
    st.markdown('<div class="filter-label">Filter Zones</div>', unsafe_allow_html=True)
    show_flood   = st.checkbox("🌊 Flood Zones",      value=True)
    show_cyclone = st.checkbox("🌀 Cyclone Warnings", value=True)
    show_safe    = st.checkbox("✅ Safe Zones",        value=True)

    st.markdown('<div class="filter-label" style="margin-top:0.8rem">Severity</div>', unsafe_allow_html=True)
    sev_filter = st.multiselect("", ["Critical","High","Moderate","None"], default=["Critical","High","Moderate","None"], label_visibility="collapsed")

    st.markdown('<div class="filter-label" style="margin-top:0.8rem">Map Style</div>', unsafe_allow_html=True)
    tile_choice = st.selectbox("", ["CartoDB dark_matter","CartoDB positron","OpenStreetMap","Stamen Terrain"], label_visibility="collapsed")

    tile_map = {
        "CartoDB dark_matter": "CartoDB dark_matter",
        "CartoDB positron":    "CartoDB positron",
        "OpenStreetMap":       "OpenStreetMap",
        "Stamen Terrain":      "Stamen Terrain",
    }

with map_col:
    # ── BUILD FOLIUM MAP ──
    m = folium.Map(
        location=[22.5, 82.5],
        zoom_start=5,
        tiles=tile_map[tile_choice],
        prefer_canvas=True,
    )

    # Filter data
    type_filter = []
    if show_flood:   type_filter.append("Flood")
    if show_cyclone: type_filter.append("Cyclone")
    if show_safe:    type_filter.append("Safe")

    filtered = df[df["type"].isin(type_filter) & df["severity"].isin(sev_filter)]

    # Layer groups
    flood_grp   = folium.FeatureGroup(name="🌊 Flood Zones",      show=show_flood)
    cyclone_grp = folium.FeatureGroup(name="🌀 Cyclone Warnings",  show=show_cyclone)
    safe_grp    = folium.FeatureGroup(name="✅ Safe Zones",         show=show_safe)
    group_map   = {"Flood": flood_grp, "Cyclone": cyclone_grp, "Safe": safe_grp}

    for _, row in filtered.iterrows():
        sty   = TYPE_STYLE[row["type"]]
        popup = folium.Popup(folium.IFrame(make_popup_html(row), width=258, height=180), max_width=260)
        tooltip = f"<b>{row['district']}</b> · {row['type']}"

        marker = folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=popup,
            tooltip=tooltip,
            icon=folium.Icon(
                color="red"   if row["type"]=="Flood"   else
                      "orange" if row["type"]=="Cyclone" else "green",
                icon=sty["icon"],
                prefix=sty["prefix"],
            ),
        )

        # Pulse circle for critical zones
        if row["severity"] == "Critical":
            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=22,
                color=sty["color"],
                fill=True,
                fill_color=sty["color"],
                fill_opacity=0.12,
                weight=1.5,
                tooltip=f"⚠️ CRITICAL — {row['district']}",
            ).add_to(group_map[row["type"]])

        marker.add_to(group_map[row["type"]])

    flood_grp.add_to(m)
    cyclone_grp.add_to(m)
    safe_grp.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)

    # ── EMBED MAP ──
    map_data = st_folium(m, width="100%", height=560, returned_objects=["last_object_clicked_popup","last_clicked"])

# ─────────────────────────────────────────────
# CLICK INFO PANEL
# ─────────────────────────────────────────────
with panel_col:
    st.markdown('<div class="filter-label" style="margin-top:1rem">Selected Zone</div>', unsafe_allow_html=True)

    clicked = map_data.get("last_clicked")
    if clicked:
        clat, clon = clicked["lat"], clicked["lng"]
        # Find nearest zone to click
        dists = ((df["lat"] - clat)**2 + (df["lon"] - clon)**2)
        nearest = df.iloc[dists.idxmin()]
        sty = TYPE_STYLE[nearest["type"]]
        st.markdown(f"""
        <div class="zone-info-card">
            <div class="zone-info-title" style="color:{sty['color']}">{nearest['district']}</div>
            <div class="zone-info-row">State: <span>{nearest['state']}</span></div>
            <div class="zone-info-row">Type: <span style="color:{sty['color']}">{nearest['type']}</span></div>
            <div class="zone-info-row">Severity: <span>{nearest['severity']}</span></div>
            <div class="zone-info-row">Population: <span>{nearest['population']:,}</span></div>
            <div class="zone-info-row">Warehouse: <span>{nearest['warehouse']}</span></div>
            <div class="zone-info-row">Updated: <span>{nearest['last_updated']}</span></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#8a90a8;font-size:0.82rem;padding:0.5rem 0">Click any marker on the map to see zone details here.</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ZONE DATA TABLE
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("#### 📋 Zone Data Table")
display_df = filtered[["district","state","type","severity","population","warehouse","last_updated"]].copy()
display_df.columns = ["District","State","Type","Severity","Population","Nearest Warehouse","Last Updated"]
st.dataframe(display_df.reset_index(drop=True), use_container_width=True, hide_index=True)
st.caption(f"Showing {len(filtered)} of {len(df)} zones · Filters active")
