import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EcoWatt India",
    page_icon="E",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Appliance data (no emojis) ────────────────────────────────────────────────
APPLIANCES = {
    "LED Bulb (9W)":            9,
    "Tube Light (40W)":         40,
    "Ceiling Fan (75W)":        75,
    "AC 1.5 Ton (1500W)":       1500,
    "LED TV 32in (60W)":        60,
    "Desktop PC (300W)":        300,
    "Laptop (65W)":             65,
    "Microwave (1200W)":        1200,
    "Electric Cooker (800W)":   800,
    "Electric Kettle (1500W)":  1500,
    "Washing Machine (500W)":   500,
    "Refrigerator 300L (150W)": 150,
    "Water Heater (2000W)":     2000,
    "Air Purifier (50W)":       50,
    "EV Charger (3300W)":       3300,
}

RATE_PER_UNIT = 6.5   # Rs / kWh

# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "prev_page" not in st.session_state:
    st.session_state.prev_page = "home"

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;700&display=swap');

:root {
    --teal:      #00C9A7;
    --teal-glow: rgba(0,201,167,0.45);
    --teal-dark: #009e83;
    --amber:     #FFB703;
    --coral:     #FF6B6B;
    --bg-glass:  rgba(255,255,255,0.93);
    --text:      #0a0a0a;
}

/* Background */
.stApp {
    background:
        linear-gradient(135deg, rgba(0,18,36,0.93) 0%, rgba(0,45,65,0.90) 100%),
        url("https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=1920&q=80")
        center/cover fixed no-repeat;
    font-family: 'Exo 2', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; }

/* Navbar */
.ecowatt-nav {
    display: flex;
    align-items: center;
    background: rgba(0,0,0,0.60);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-bottom: 2px solid var(--teal);
    border-radius: 0 0 18px 18px;
    padding: 14px 32px;
    margin-bottom: 28px;
    box-shadow: 0 4px 32px rgba(0,201,167,0.18);
}
.ecowatt-logo {
    font-family: 'Orbitron', monospace;
    font-size: 1.7rem;
    font-weight: 900;
    color: var(--teal);
    letter-spacing: 3px;
    text-shadow: 0 0 18px var(--teal-glow);
}
.ecowatt-logo span { color: #ffffff; }
.nav-tagline {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.65);
    letter-spacing: 2px;
    margin-top: -4px;
}

/* Slide animation */
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(55px); }
    to   { opacity: 1; transform: translateX(0); }
}
.page-wrapper { animation: slideInRight 0.45s cubic-bezier(0.25,0.8,0.25,1) both; }

/* Glass card */
.glass-card {
    background: var(--bg-glass);
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    border-radius: 20px;
    border: 1.5px solid rgba(0,201,167,0.40);
    padding: 28px 32px;
    margin-bottom: 22px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.28);
    color: var(--text) !important;
}
.glass-card * { color: var(--text) !important; }

/* Stat row */
.stat-row { display: flex; gap: 16px; margin: 18px 0; flex-wrap: wrap; }
.stat-card {
    flex: 1; min-width: 130px;
    background: linear-gradient(135deg, rgba(0,201,167,0.18), rgba(0,201,167,0.06));
    border: 2px solid var(--teal);
    border-radius: 16px;
    padding: 18px 14px;
    text-align: center;
    transition: transform 0.25s, box-shadow 0.25s;
    backdrop-filter: blur(12px);
}
.stat-card:hover { transform: translateY(-5px); box-shadow: 0 8px 28px var(--teal-glow); }
.stat-value {
    font-family: 'Orbitron', monospace;
    font-size: 1.85rem;
    font-weight: 700;
    color: var(--teal) !important;
    text-shadow: 0 0 12px var(--teal-glow);
}
.stat-label {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.85) !important;
    margin-top: 5px;
    letter-spacing: 1px;
    font-weight: 600;
}

/* Main buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--teal), var(--teal-dark)) !important;
    color: #000000 !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 0.80rem !important;
    letter-spacing: 2px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 26px !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 4px 18px rgba(0,201,167,0.30) !important;
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.03) !important;
    box-shadow: 0 0 0 3px var(--teal), 0 8px 28px var(--teal-glow) !important;
}

/* Nav buttons */
.nav-btn > button {
    background: transparent !important;
    color: #ffffff !important;
    border: 1.5px solid rgba(255,255,255,0.28) !important;
    font-size: 0.74rem !important;
    padding: 7px 18px !important;
    box-shadow: none !important;
}
.nav-btn > button:hover {
    border-color: var(--teal) !important;
    color: var(--teal) !important;
    box-shadow: 0 0 14px var(--teal-glow) !important;
    transform: translateY(-2px) !important;
}

/* ALL INPUTS: white bg, black text, teal border */
input, textarea,
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea,
div[data-baseweb="select"] input,
.stNumberInput input,
.stTextInput input {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 2.5px solid var(--teal) !important;
    border-radius: 8px !important;
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    caret-color: #000000 !important;
}
input:focus, textarea:focus,
div[data-baseweb="input"] input:focus,
.stNumberInput input:focus {
    background-color: #ffffff !important;
    color: #000000 !important;
    box-shadow: 0 0 0 3px var(--teal-glow) !important;
    outline: none !important;
}

/* Multiselect */
div[data-baseweb="select"] > div,
div[data-baseweb="select"] [role="combobox"] {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 2.5px solid var(--teal) !important;
    border-radius: 8px !important;
}
div[data-baseweb="tag"] {
    background-color: var(--teal) !important;
    color: #000000 !important;
    font-weight: 700 !important;
}
div[data-baseweb="select"] [role="option"] { background: #fff !important; color: #000 !important; }
div[data-baseweb="select"] [role="option"]:hover { background: rgba(0,201,167,0.14) !important; }
div[data-baseweb="popover"] {
    background: #ffffff !important;
    border: 2px solid var(--teal) !important;
    border-radius: 10px !important;
}

/* Number input wrapper */
.stNumberInput > div > div {
    background: #ffffff !important;
    border: 2.5px solid var(--teal) !important;
    border-radius: 8px !important;
}
.stNumberInput button {
    background: rgba(0,201,167,0.14) !important;
    color: #000 !important;
    border: none !important;
}

/* Labels — pitch black for max visibility */
.stMultiSelect label, .stNumberInput label, .stSelectbox label,
.stTextInput label, .stSlider label {
    color: #000000 !important;
    font-weight: 700 !important;
    font-size: 0.93rem !important;
}

/* Section titles */
.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.05rem;
    font-weight: 700;
    color: #000000 !important;
    letter-spacing: 2px;
    border-bottom: 2.5px solid var(--teal);
    padding-bottom: 8px;
    margin-bottom: 18px;
}

/* Tip cards */
.tip-card {
    border-radius: 12px;
    padding: 14px 18px;
    margin: 10px 0;
    border-left: 5px solid;
    font-weight: 600;
    font-size: 0.95rem;
    color: #000000 !important;
    line-height: 1.65;
}
.tip-1 { background: rgba(0,201,167,0.14);  border-color: var(--teal); }
.tip-2 { background: rgba(255,183,3,0.14);  border-color: var(--amber); }
.tip-3 { background: rgba(255,107,107,0.14);border-color: var(--coral); }
.tip-card b { color: #000000 !important; }

/* Hero */
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(1.9rem, 5vw, 3.4rem);
    font-weight: 900;
    color: #ffffff;
    line-height: 1.15;
    text-shadow: 0 0 40px var(--teal-glow);
    margin-bottom: 14px;
}
.hero-title .accent { color: var(--teal); }
.hero-sub {
    font-size: 1.05rem;
    color: rgba(255,255,255,0.85);
    max-width: 580px;
    line-height: 1.75;
}

/* Feature grid */
.feat-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 18px; margin-top: 26px; }
.feat-item {
    background: rgba(255,255,255,0.92);
    border-radius: 14px;
    border: 1.5px solid rgba(0,201,167,0.40);
    padding: 22px 18px;
    text-align: center;
    transition: transform 0.25s, box-shadow 0.25s;
}
.feat-item:hover { transform: translateY(-6px); box-shadow: 0 12px 36px var(--teal-glow); }
.feat-icon {
    font-size: 1rem; font-weight: 900; color: var(--teal) !important;
    margin-bottom: 10px; font-family:'Orbitron',monospace;
    letter-spacing: 2px;
}
.feat-title { font-weight: 700; font-size: 0.93rem; color: #000000 !important; margin-bottom: 6px; }
.feat-desc  { font-size: 0.80rem; color: #111111 !important; line-height: 1.55; }

/* AI culprit badge */
.culprit-badge {
    background: linear-gradient(135deg, rgba(255,107,107,0.16), rgba(255,183,3,0.10));
    border: 2px solid var(--coral);
    border-radius: 14px;
    padding: 16px 22px;
    margin: 16px 0;
    font-size: 1rem;
    font-weight: 700;
    color: #000000 !important;
    line-height: 1.65;
}
.culprit-badge b { color: #000000 !important; }
.culprit-name { color: #c0392b !important; font-size: 1.05rem; font-weight: 800; }

/* Compare header */
.compare-header {
    font-family: 'Orbitron', monospace;
    font-size: 0.72rem;
    color: var(--teal) !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
    font-weight: 700;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); }
::-webkit-scrollbar-thumb { background: var(--teal); border-radius: 6px; }

.js-plotly-plot .plotly, .js-plotly-plot .plotly .main-svg { background: transparent !important; }
</style>
""", unsafe_allow_html=True)


# ── Navigation helper ─────────────────────────────────────────────────────────
def nav_to(page: str):
    st.session_state.prev_page = st.session_state.page
    st.session_state.page = page


# ── Navbar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ecowatt-nav">
  <div>
    <div class="ecowatt-logo">EcoWatt<span> India</span></div>
    <div class="nav-tagline">PREMIUM ENERGY ANALYTICS PLATFORM</div>
  </div>
</div>
""", unsafe_allow_html=True)

col_n1, col_n2, col_n3, _spacer = st.columns([1, 1, 1, 6])
with col_n1:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("HOME"):
        nav_to("home")
    st.markdown('</div>', unsafe_allow_html=True)
with col_n2:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("CALCULATE"):
        nav_to("calculate")
    st.markdown('</div>', unsafe_allow_html=True)
with col_n3:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("COMPARE"):
        nav_to("compare")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")


# ══════════════════════════════════════════════════════════════════════════════
#  HOME
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 40px 0 22px 0;">
      <div class="hero-title">Smart Energy.<br><span class="accent">Zero Waste.</span><br>Lower Bills.</div>
      <div class="hero-sub">
        Track, analyse, and slash your electricity bills with India's most intelligent
        energy management platform — powered by real-time analytics and AI auditing.
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("START CALCULATING"):
            nav_to("calculate")
    with c2:
        if st.button("COMPARE MONTHS"):
            nav_to("compare")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-row">
      <div class="stat-card">
        <div class="stat-value">Rs 8.2K</div>
        <div class="stat-label">AVG MONTHLY BILL SAVED</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">15+</div>
        <div class="stat-label">APPLIANCES TRACKED</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">AI</div>
        <div class="stat-label">SMART AUDIT ENGINE</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">Rs 6.5</div>
        <div class="stat-label">PER UNIT RATE (kWh)</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feat-grid">
      <div class="feat-item">
        <div class="feat-icon">CALC</div>
        <div class="feat-title">INSTANT CALCULATOR</div>
        <div class="feat-desc">Select appliances, enter daily hours and get your monthly bill in seconds.</div>
      </div>
      <div class="feat-item">
        <div class="feat-icon">CHART</div>
        <div class="feat-title">ANIMATED CHARTS</div>
        <div class="feat-desc">Beautiful Plotly bar and area charts that grow on load for deep insights.</div>
      </div>
      <div class="feat-item">
        <div class="feat-icon">AI</div>
        <div class="feat-title">AI AUDIT ENGINE</div>
        <div class="feat-desc">Identifies the culprit appliance and gives bold, actionable saving tips.</div>
      </div>
      <div class="feat-item">
        <div class="feat-icon">VS</div>
        <div class="feat-title">DEEP COMPARISON</div>
        <div class="feat-desc">Side-by-side last vs this month comparison with full change analysis.</div>
      </div>
      <div class="feat-item">
        <div class="feat-icon">CO2</div>
        <div class="feat-title">CO2 TRACKER</div>
        <div class="feat-desc">See your carbon footprint and how much CO2 you can prevent each month.</div>
      </div>
      <div class="feat-item">
        <div class="feat-icon">UI</div>
        <div class="feat-title">PREMIUM UI</div>
        <div class="feat-desc">Glassmorphism cards, slide transitions, and teal glow micro-interactions.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  CALCULATE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "calculate":
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
      <div class="section-title">ENERGY CALCULATOR</div>
      <p style="color:#000000;margin-bottom:0;font-weight:600;">
        Select your appliances and enter daily usage hours for each one.
        Your bill and CO2 footprint are computed instantly.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Appliance selector
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">SELECT APPLIANCES</div>', unsafe_allow_html=True)
    selected = st.multiselect(
        "Choose appliances used in your home:",
        list(APPLIANCES.keys()),
        key="calc_selected",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    hours_data: dict[str, float] = {}

    # ── Inline row per appliance: name column | hours column ─────────────────
    if selected:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">DAILY USAGE HOURS</div>', unsafe_allow_html=True)
        st.markdown(
            '<p style="color:#000000;font-weight:600;margin-bottom:14px;">'
            'Enter how many hours each appliance runs per day:</p>',
            unsafe_allow_html=True,
        )

        # Column headers
        h1, h2 = st.columns([3, 2])
        with h1:
            st.markdown(
                '<div style="font-family:Orbitron,monospace;font-size:0.70rem;'
                'color:#00C9A7;letter-spacing:2px;font-weight:700;padding:2px 14px 8px;">APPLIANCE</div>',
                unsafe_allow_html=True,
            )
        with h2:
            st.markdown(
                '<div style="font-family:Orbitron,monospace;font-size:0.70rem;'
                'color:#00C9A7;letter-spacing:2px;font-weight:700;padding:2px 0 8px;">HOURS / DAY</div>',
                unsafe_allow_html=True,
            )

        for appliance in selected:
            col_name, col_input = st.columns([3, 2])
            with col_name:
                st.markdown(
                    f'<div style="display:flex;align-items:center;height:52px;'
                    f'font-weight:700;font-size:0.95rem;color:#000000;'
                    f'background:rgba(0,201,167,0.08);border:1.5px solid rgba(0,201,167,0.30);'
                    f'border-radius:8px;padding:0 14px;">{appliance}</div>',
                    unsafe_allow_html=True,
                )
            with col_input:
                h = st.number_input(
                    "hrs",
                    min_value=0.0,
                    max_value=24.0,
                    value=4.0,
                    step=0.5,
                    key=f"calc_h_{appliance}",
                    label_visibility="collapsed",
                )
                hours_data[appliance] = h

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Calculations ──────────────────────────────────────────────────────
        days = 30
        rows = []
        for app, h in hours_data.items():
            watts = APPLIANCES[app]
            units = (watts * h * days) / 1000
            cost  = units * RATE_PER_UNIT
            co2   = units * 0.82
            rows.append({
                "Appliance":   app,
                "Watts":       watts,
                "Hours/Day":   h,
                "Units (kWh)": round(units, 2),
                "Cost (Rs)":   round(cost, 2),
                "CO2 (kg)":    round(co2, 2),
            })

        df = pd.DataFrame(rows).sort_values("Cost (Rs)", ascending=False)
        total_units = df["Units (kWh)"].sum()
        total_cost  = df["Cost (Rs)"].sum()
        total_co2   = df["CO2 (kg)"].sum()

        # Summary stats
        st.markdown(f"""
        <div class="stat-row">
          <div class="stat-card">
            <div class="stat-value">{total_units:.1f}</div>
            <div class="stat-label">TOTAL UNITS (kWh)</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">Rs {total_cost:,.0f}</div>
            <div class="stat-label">ESTIMATED MONTHLY BILL</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{total_co2:.1f} kg</div>
            <div class="stat-label">CO2 FOOTPRINT</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{len(selected)}</div>
            <div class="stat-label">APPLIANCES TRACKED</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Animated bar chart ────────────────────────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">COST BREAKDOWN</div>', unsafe_allow_html=True)

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=df["Appliance"],
            y=df["Cost (Rs)"],
            marker=dict(
                color=df["Cost (Rs)"],
                colorscale="Teal",
                showscale=False,
                line=dict(color="#00C9A7", width=1.5),
            ),
            text=[f"Rs {v:,.0f}" for v in df["Cost (Rs)"]],
            textposition="outside",
            textfont=dict(color="#000000", size=12, family="Exo 2"),
            hovertemplate="<b>%{x}</b><br>Cost: Rs %{y:,.0f}<extra></extra>",
        ))
        fig_bar.frames = [
            go.Frame(data=[go.Bar(y=df["Cost (Rs)"] * (k / 20))], name=str(k))
            for k in range(1, 21)
        ]
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Exo 2", color="#000000"),
            xaxis=dict(tickangle=-35, tickfont=dict(size=11, color="#000000"),
                       gridcolor="rgba(0,0,0,0.08)", linecolor="rgba(0,201,167,0.4)"),
            yaxis=dict(title="Rs Cost", tickfont=dict(color="#000000"),
                       gridcolor="rgba(0,0,0,0.08)", linecolor="rgba(0,201,167,0.4)"),
            margin=dict(t=50, b=90, l=70, r=20),
            updatemenus=[dict(
                type="buttons", showactive=False, y=1.12, x=0,
                buttons=[dict(
                    label="PLAY ANIMATION",
                    method="animate",
                    args=[None, {"frame": {"duration": 60, "redraw": True},
                                 "fromcurrent": True, "transition": {"duration": 30}}]
                )]
            )],
            height=420,
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Area chart ────────────────────────────────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">ENERGY UNITS — AREA VIEW</div>', unsafe_allow_html=True)

        df_s = df.sort_values("Appliance")
        fig_area = go.Figure()
        fig_area.add_trace(go.Scatter(
            x=df_s["Appliance"], y=df_s["Units (kWh)"],
            name="Units (kWh)",
            fill="tozeroy", mode="lines+markers",
            line=dict(color="#00C9A7", width=3),
            fillcolor="rgba(0,201,167,0.16)",
            marker=dict(size=10, color="#00C9A7", line=dict(color="#000", width=1.5)),
            hovertemplate="<b>%{x}</b><br>%{y:.2f} kWh<extra></extra>",
        ))
        fig_area.add_trace(go.Scatter(
            x=df_s["Appliance"], y=df_s["CO2 (kg)"],
            name="CO2 (kg)",
            fill="tozeroy", mode="lines+markers",
            line=dict(color="#FF6B6B", width=2.5, dash="dot"),
            fillcolor="rgba(255,107,107,0.10)",
            marker=dict(size=8, color="#FF6B6B"),
            hovertemplate="<b>%{x}</b><br>CO2: %{y:.2f} kg<extra></extra>",
        ))
        fig_area.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Exo 2", color="#000000"),
            xaxis=dict(tickangle=-35, tickfont=dict(color="#000000"),
                       gridcolor="rgba(0,0,0,0.08)"),
            yaxis=dict(tickfont=dict(color="#000000"), gridcolor="rgba(0,0,0,0.08)"),
            legend=dict(bgcolor="rgba(255,255,255,0.85)", bordercolor="#00C9A7",
                        borderwidth=1, font=dict(color="#000000")),
            margin=dict(t=20, b=90, l=60, r=20), height=380,
        )
        st.plotly_chart(fig_area, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── AI Auditor ────────────────────────────────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">AI ENERGY AUDITOR REPORT</div>', unsafe_allow_html=True)

        culprit     = df.iloc[0]
        culprit_pct = (culprit["Cost (Rs)"] / total_cost * 100) if total_cost > 0 else 0
        watts       = APPLIANCES[culprit["Appliance"]]
        saving_1hr  = round((watts * 1 * 30 / 1000) * RATE_PER_UNIT, 0)

        st.markdown(f"""
        <div class="culprit-badge">
          CULPRIT APPLIANCE IDENTIFIED:
          <span class="culprit-name">&nbsp;{culprit["Appliance"]}</span><br><br>
          This appliance accounts for <b>{culprit_pct:.1f}%</b> of your total bill,
          costing <b>Rs {culprit["Cost (Rs)"]:,.0f}/month</b>
          at {culprit["Hours/Day"]} hrs/day.
        </div>
        """, unsafe_allow_html=True)

        tip1 = (f"Reduce <b>{culprit['Appliance']}</b> by 1 hour/day "
                f"and save <b>Rs {saving_1hr:,.0f}/month</b> immediately.")
        tip2 = ("Upgrade to a <b>5-star BEE-rated</b> equivalent. "
                "Indian 5-star models use up to <b>40% less energy</b> than standard ones.")
        tip3 = ("Use a <b>smart plug timer</b> to cut power during off-peak hours. "
                "This prevents phantom standby drain worth <b>Rs 200 to 500/month</b>.")

        if watts >= 1000:
            tip2 = (f"Set a thermostat timer on your {culprit['Appliance'].split('(')[0].strip()}. "
                    "Each degree of optimisation saves up to <b>Rs 350/month</b>.")
        if total_co2 > 50:
            tip3 = (f"Your carbon footprint is <b>{total_co2:.1f} kg CO2/month</b>. "
                    "A 1 kW rooftop solar panel offsets ~90 kg CO2 and cuts bills by Rs 1,500+.")

        st.markdown(f"""
        <div class="tip-card tip-1"><b>TIP 1 — QUICK WIN:</b><br>{tip1}</div>
        <div class="tip-card tip-2"><b>TIP 2 — UPGRADE STRATEGY:</b><br>{tip2}</div>
        <div class="tip-card tip-3"><b>TIP 3 — SMART HABIT:</b><br>{tip3}</div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="compare-header">DETAILED BREAKDOWN TABLE</div>', unsafe_allow_html=True)
        st.dataframe(
            df[["Appliance", "Watts", "Hours/Day", "Units (kWh)", "Cost (Rs)", "CO2 (kg)"]],
            use_container_width=True,
            hide_index=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:52px 32px;">
          <div style="font-family:'Orbitron',monospace;font-size:1.6rem;
                      color:#00C9A7;margin-bottom:14px;letter-spacing:4px;">
            SELECT APPLIANCES ABOVE
          </div>
          <div style="color:#000000;font-weight:600;font-size:1rem;line-height:1.7;">
            Choose one or more appliances from the list.<br>
            A daily-hours input will appear for each one instantly.
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  COMPARE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "compare":
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
      <div class="section-title">DEEP COMPARISON MODE</div>
      <p style="color:#000000;font-weight:600;margin-bottom:0;">
        Enter daily usage hours for <b>Last Month</b> and <b>This Month</b> for each appliance.
        The AI will identify what drove your bill up.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">SELECT APPLIANCES TO COMPARE</div>', unsafe_allow_html=True)
    comp_selected = st.multiselect(
        "Choose appliances for month-on-month comparison:",
        list(APPLIANCES.keys()),
        key="comp_selected",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    last_hours: dict[str, float] = {}
    this_hours: dict[str, float] = {}

    if comp_selected:
        # ── Inline 3-column row: appliance | last month | this month ─────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">ENTER HOURS PER APPLIANCE</div>', unsafe_allow_html=True)

        hdr_name, hdr_last, hdr_this = st.columns([3, 2, 2])
        with hdr_name:
            st.markdown(
                '<div style="font-family:Orbitron,monospace;font-size:0.70rem;'
                'color:#00C9A7;letter-spacing:2px;font-weight:700;padding:2px 14px 8px;">APPLIANCE</div>',
                unsafe_allow_html=True,
            )
        with hdr_last:
            st.markdown(
                '<div style="font-family:Orbitron,monospace;font-size:0.70rem;'
                'color:#4DAFFF;letter-spacing:2px;font-weight:700;padding:2px 0 8px;">LAST MONTH (hrs/day)</div>',
                unsafe_allow_html=True,
            )
        with hdr_this:
            st.markdown(
                '<div style="font-family:Orbitron,monospace;font-size:0.70rem;'
                'color:#00C9A7;letter-spacing:2px;font-weight:700;padding:2px 0 8px;">THIS MONTH (hrs/day)</div>',
                unsafe_allow_html=True,
            )

        for app in comp_selected:
            col_name, col_last, col_this = st.columns([3, 2, 2])
            with col_name:
                st.markdown(
                    f'<div style="display:flex;align-items:center;height:52px;'
                    f'font-weight:700;font-size:0.95rem;color:#000000;'
                    f'background:rgba(0,201,167,0.07);border:1.5px solid rgba(0,201,167,0.28);'
                    f'border-radius:8px;padding:0 14px;">{app}</div>',
                    unsafe_allow_html=True,
                )
            with col_last:
                lh = st.number_input(
                    "Last", min_value=0.0, max_value=24.0, value=4.0, step=0.5,
                    key=f"last_{app}", label_visibility="collapsed",
                )
                last_hours[app] = lh
            with col_this:
                th = st.number_input(
                    "This", min_value=0.0, max_value=24.0, value=4.0, step=0.5,
                    key=f"this_{app}", label_visibility="collapsed",
                )
                this_hours[app] = th

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Build comparison dataframe ─────────────────────────────────────────
        days = 30
        cmp_rows = []
        for app in comp_selected:
            w  = APPLIANCES[app]
            lh = last_hours[app]
            th = this_hours[app]
            l_units = round((w * lh * days) / 1000, 2)
            t_units = round((w * th * days) / 1000, 2)
            l_cost  = round(l_units * RATE_PER_UNIT, 2)
            t_cost  = round(t_units * RATE_PER_UNIT, 2)
            delta   = round(t_cost - l_cost, 2)
            cmp_rows.append({
                "Appliance":       app,
                "Last Month (Rs)": l_cost,
                "This Month (Rs)": t_cost,
                "Change (Rs)":     delta,
                "Last kWh":        l_units,
                "This kWh":        t_units,
            })

        cdf = pd.DataFrame(cmp_rows).sort_values("Change (Rs)", ascending=False)
        total_last  = cdf["Last Month (Rs)"].sum()
        total_this  = cdf["This Month (Rs)"].sum()
        total_delta = total_this - total_last
        arrow       = "UP" if total_delta >= 0 else "DOWN"
        col_d       = "#c0392b" if total_delta >= 0 else "#009e83"

        st.markdown(f"""
        <div class="stat-row">
          <div class="stat-card">
            <div class="stat-value">Rs {total_last:,.0f}</div>
            <div class="stat-label">LAST MONTH TOTAL</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">Rs {total_this:,.0f}</div>
            <div class="stat-label">THIS MONTH TOTAL</div>
          </div>
          <div class="stat-card">
            <div class="stat-value" style="color:{col_d};">{arrow} Rs {abs(total_delta):,.0f}</div>
            <div class="stat-label">NET CHANGE</div>
          </div>
          <div class="stat-card">
            <div class="stat-value" style="color:{col_d};">
              {'+' if total_delta>=0 else ''}{(total_delta/total_last*100) if total_last else 0:.1f}%
            </div>
            <div class="stat-label">PERCENTAGE CHANGE</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Grouped bar ───────────────────────────────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">SIDE-BY-SIDE COST COMPARISON</div>', unsafe_allow_html=True)

        fig_grp = go.Figure()
        fig_grp.add_trace(go.Bar(
            name="Last Month", x=cdf["Appliance"], y=cdf["Last Month (Rs)"],
            marker_color="rgba(100,180,255,0.85)",
            marker_line=dict(color="#4DAFFF", width=1.5),
            text=[f"Rs {v:,.0f}" for v in cdf["Last Month (Rs)"]],
            textposition="outside", textfont=dict(color="#000000", size=10),
        ))
        fig_grp.add_trace(go.Bar(
            name="This Month", x=cdf["Appliance"], y=cdf["This Month (Rs)"],
            marker_color="rgba(0,201,167,0.85)",
            marker_line=dict(color="#00C9A7", width=1.5),
            text=[f"Rs {v:,.0f}" for v in cdf["This Month (Rs)"]],
            textposition="outside", textfont=dict(color="#000000", size=10),
        ))
        fig_grp.update_layout(
            barmode="group", bargap=0.22,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Exo 2", color="#000000"),
            xaxis=dict(tickangle=-35, tickfont=dict(color="#000000"),
                       gridcolor="rgba(0,0,0,0.06)"),
            yaxis=dict(tickfont=dict(color="#000000"), title="Rs Cost",
                       gridcolor="rgba(0,0,0,0.06)"),
            legend=dict(bgcolor="rgba(255,255,255,0.85)", bordercolor="#00C9A7",
                        borderwidth=1, font=dict(color="#000000")),
            margin=dict(t=30, b=90, l=60, r=20), height=420,
        )
        st.plotly_chart(fig_grp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Delta chart ───────────────────────────────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">CHANGE ANALYSIS</div>', unsafe_allow_html=True)

        bar_colors = ["#c0392b" if v >= 0 else "#009e83" for v in cdf["Change (Rs)"]]
        fig_delta = go.Figure(go.Bar(
            x=cdf["Appliance"], y=cdf["Change (Rs)"],
            marker_color=bar_colors,
            marker_line=dict(color="#000", width=0.8),
            text=[f"{'+' if v>=0 else ''}Rs {v:,.0f}" for v in cdf["Change (Rs)"]],
            textposition="outside",
            textfont=dict(color="#000000", size=11, family="Exo 2"),
            hovertemplate="<b>%{x}</b><br>Change Rs %{y:,.0f}<extra></extra>",
        ))
        fig_delta.add_hline(y=0, line_dash="dash", line_color="rgba(0,0,0,0.35)", line_width=1.5)
        fig_delta.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Exo 2", color="#000000"),
            xaxis=dict(tickangle=-35, tickfont=dict(color="#000000"),
                       gridcolor="rgba(0,0,0,0.06)"),
            yaxis=dict(tickfont=dict(color="#000000"), title="Change (Rs)",
                       gridcolor="rgba(0,0,0,0.06)", zeroline=False),
            margin=dict(t=30, b=90, l=60, r=20), height=380,
        )
        st.plotly_chart(fig_delta, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── AI Auditor ────────────────────────────────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">AI AUDITOR — COMPARISON REPORT</div>', unsafe_allow_html=True)

        culprit_row = (cdf[cdf["Change (Rs)"] > 0].iloc[0]
                       if (cdf["Change (Rs)"] > 0).any() else None)

        if culprit_row is not None:
            cn    = culprit_row["Appliance"]
            cd    = culprit_row["Change (Rs)"]
            clast = last_hours[cn]
            cthis = this_hours[cn]
            st.markdown(f"""
            <div class="culprit-badge">
              MONTH-ON-MONTH CULPRIT:
              <span class="culprit-name">&nbsp;{cn}</span><br><br>
              Usage rose from <b>{clast} hrs/day to {cthis} hrs/day</b>,
              adding <b>Rs {cd:,.0f}</b> to your bill this month.
            </div>
            <div class="tip-card tip-1">
              <b>TIP 1 — REVERT USAGE:</b><br>
              Bring <b>{cn}</b> back to {clast} hrs/day and immediately recover
              <b>Rs {cd:,.0f}/month</b>.
            </div>
            <div class="tip-card tip-2">
              <b>TIP 2 — SCHEDULE SMARTLY:</b><br>
              Use off-peak hours (10 PM to 6 AM) for high-wattage appliances.
              Many Indian DISCOMs offer a <b>15 to 25% Time-of-Day discount</b> in night slots.
            </div>
            <div class="tip-card tip-3">
              <b>TIP 3 — SET A BUDGET ALERT:</b><br>
              Set a Rs {int(total_last * 1.05):,} monthly energy budget in a smart meter app.
              Real-time alerts prevent bill shock before the cycle ends.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="tip-card tip-1">
              <b>GREAT RESULT!</b><br>
              Your usage did not increase for any appliance this month.
              Keep up these habits to continue saving energy and money.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="compare-header">DETAILED COMPARISON TABLE</div>', unsafe_allow_html=True)
        st.dataframe(
            cdf[["Appliance", "Last Month (Rs)", "This Month (Rs)",
                 "Change (Rs)", "Last kWh", "This kWh"]],
            use_container_width=True,
            hide_index=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:52px 32px;">
          <div style="font-family:'Orbitron',monospace;font-size:1.6rem;
                      color:#00C9A7;margin-bottom:14px;letter-spacing:4px;">
            SELECT APPLIANCES ABOVE
          </div>
          <div style="color:#000000;font-weight:600;font-size:1rem;line-height:1.7;">
            Choose appliances to begin your month-on-month comparison.<br>
            Side-by-side inputs, charts and AI report will appear instantly.
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:48px;padding:20px;
            color:rgba(255,255,255,0.55);font-size:0.72rem;
            font-family:'Exo 2',sans-serif;letter-spacing:2px;">
  ECOWATT INDIA &nbsp; · &nbsp; PREMIUM ENERGY ANALYTICS &nbsp; · &nbsp;
  BUILT WITH STREAMLIT + PLOTLY &nbsp; · &nbsp; RATE: RS 6.5/kWh
</div>
""", unsafe_allow_html=True)
