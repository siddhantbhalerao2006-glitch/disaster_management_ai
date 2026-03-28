import streamlit as st

# ── Demo controls (remove in production; set st.session_state.prediction from your ML model) ──
if "prediction" not in st.session_state:
    st.session_state.prediction = "Flood"

# ─────────────────────────────────────────────
# ALERT CONFIG — extend this dict to add more disaster types
# ─────────────────────────────────────────────
ALERT_CONFIG = {
    "Flood": {
        "bg":      "#7f1d1d",          # deep red
        "border":  "#ef4444",
        "glow":    "#ef444440",
        "icon":    "🌊",
        "heading": "FLOOD ALERT",
        "message": "Evacuate Immediately. Move to higher ground. Avoid flooded roads.",
        "pulse":   True,               # animated pulse for critical alerts
    },
    "Cyclone": {
        "bg":      "#7c2d12",          # deep orange
        "border":  "#f97316",
        "glow":    "#f9731640",
        "icon":    "🌀",
        "heading": "CYCLONE WARNING",
        "message": "Seek sturdy shelter. Stay away from windows and coastal areas.",
        "pulse":   True,
    },
    "Landslide": {
        "bg":      "#713f12",          # deep amber/yellow
        "border":  "#eab308",
        "glow":    "#eab30840",
        "icon":    "⛰️",
        "heading": "LANDSLIDE WATCH",
        "message": "Avoid hill roads and slopes. Monitor official advisories closely.",
        "pulse":   False,
    },
}

# ─────────────────────────────────────────────
# RENDER BANNER
# ─────────────────────────────────────────────
def render_alert_banner(prediction: str) -> None:
    """
    Renders a full-width disaster alert banner based on ML model prediction
    stored in st.session_state.prediction.

    Args:
        prediction: One of 'Flood', 'Cyclone', 'Landslide'
                    (or any key added to ALERT_CONFIG).
    """
    cfg = ALERT_CONFIG.get(prediction)

    if cfg is None:
        # Unknown prediction — show a neutral fallback
        st.info(f"ℹ️ Alert system active. Prediction received: **{prediction}**")
        return

    pulse_keyframes = """
    @keyframes pulse-border {
        0%   { box-shadow: 0 0 0 0 VAR; }
        70%  { box-shadow: 0 0 0 10px transparent; }
        100% { box-shadow: 0 0 0 0 transparent; }
    }
    """.replace("VAR", cfg["glow"])

    pulse_css = f"animation: pulse-border 1.6s ease-out infinite;" if cfg["pulse"] else ""

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

    {pulse_keyframes}

    .dn-alert-banner {{
        display: flex;
        align-items: center;
        gap: 1.1rem;
        background: {cfg['bg']};
        border: 2px solid {cfg['border']};
        border-radius: 14px;
        padding: 1.1rem 1.5rem;
        margin-bottom: 1.6rem;
        {pulse_css}
    }}
    .dn-alert-icon {{
        font-size: 2.2rem;
        line-height: 1;
        flex-shrink: 0;
    }}
    .dn-alert-body {{
        flex: 1;
    }}
    .dn-alert-heading {{
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 1.15rem;
        letter-spacing: 0.06em;
        color: {cfg['border']};
        margin-bottom: 3px;
    }}
    .dn-alert-message {{
        font-family: 'DM Sans', sans-serif;
        font-size: 0.88rem;
        color: #f3f4f6;
        opacity: 0.9;
    }}
    .dn-alert-badge {{
        font-family: 'Syne', sans-serif;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        background: {cfg['border']}22;
        border: 1px solid {cfg['border']}88;
        color: {cfg['border']};
        border-radius: 20px;
        padding: 4px 12px;
        flex-shrink: 0;
        white-space: nowrap;
    }}
    </style>

    <div class="dn-alert-banner" role="alert" aria-live="assertive">
        <div class="dn-alert-icon">{cfg['icon']}</div>
        <div class="dn-alert-body">
            <div class="dn-alert-heading">{cfg['heading']}</div>
            <div class="dn-alert-message">{cfg['message']}</div>
        </div>
        <div class="dn-alert-badge">ML Detected</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN — demo harness
# ─────────────────────────────────────────────
st.set_page_config(page_title="Disaster Alert Banner", layout="wide")

# ── Banner renders first, above everything ──
render_alert_banner(st.session_state.prediction)

# ── Demo switcher (replace with your ML pipeline in production) ──
st.markdown("#### 🔬 Simulate ML Model Output")
col1, col2 = st.columns([2, 3])
with col1:
    choice = st.selectbox(
        "Set st.session_state.prediction",
        ["Flood", "Cyclone", "Landslide"],
        index=["Flood", "Cyclone", "Landslide"].index(st.session_state.prediction),
    )
    if choice != st.session_state.prediction:
        st.session_state.prediction = choice
        st.rerun()

with col2:
    st.code(f'st.session_state.prediction = "{st.session_state.prediction}"', language="python")

st.divider()
st.caption("In production: set `st.session_state.prediction` from your ML model output, then call `render_alert_banner(st.session_state.prediction)` at the top of your page.")
