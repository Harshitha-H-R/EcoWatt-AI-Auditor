import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="EcoWatt India",
    page_icon="E",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

RATE_PER_UNIT = 6.5

if "page" not in st.session_state:
    st.session_state.page = "home"
if "prev_page" not in st.session_state:
    st.session_state.prev_page = "home"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;700&display=swap');

:root {
    --teal:       #00C9A7;
    --teal-glow:  rgba(0,201,167,0.5);
    --teal-dark:  #009e83;
    --teal-dim:   rgba(0,201,167,0.15);
    --amber:      #FFB703;
    --coral:      #FF6B6B;
    --white:      #ffffff;
    --off-white:  rgba(255,255,255,0.90);
    --muted:      rgba(255,255,255,0.60);
    --card-bg:    rgba(10,28,48,0.78);
    --card-border:rgba(0,201,167,0.35);
}

/* ── App background ── */
.stApp {
    background:
        linear-gradient(135deg, rgba(0,12,28,0.96) 0%, rgba(0,35,55,0.94) 100%),
        url("https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=1920&q=80")
        center/cover fixed no-repeat;
    font-family: 'Exo 2', sans-serif;
    color: var(--white);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0.5rem !important; padding-bottom: 2rem !important; }

/* ── Navbar ── */
.ecowatt-nav {
    display: flex;
    align-items: center;
    background: rgba(0,0,0,0.70);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 2px solid var(--teal);
    border-radius: 0 0 16px 16px;
    padding: 14px 32px;
    margin-bottom: 24px;
    box-shadow: 0 4px 32px rgba(0,201,167,0.20);
}
.ecowatt-logo {
    font-family: 'Orbitron', monospace;
    font-size: 1.65rem;
    font-weight: 900;
    color: var(--teal);
    letter-spacing: 3px;
    text-shadow: 0 0 20px var(--teal-glow);
}
.ecowatt-logo span { color: #ffffff; }
.nav-tagline {
    font-size: 0.70rem;
    color: var(--muted);
    letter-spacing: 2px;
    margin-top: -3px;
}

/* ── Slide-in animation ── */
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(55px); }
    to   { opacity: 1; transform: translateX(0); }
}
.page-wrapper { animation: slideInRight 0.42s cubic-bezier(0.25,0.8,0.25,1) both; }

/* ── Glass card — DARK with WHITE text ── */
.glass-card {
    background: var(--card-bg);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border-radius: 18px;
    border: 1.5px solid var(--card-border);
    padding: 26px 30px;
    margin-bottom: 20px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.45), 0 0 0 1px rgba(255,255,255,0.04);
}

/* ── Typography inside cards ── */
.glass-card p,
.glass-card li,
.glass-card div { color: var(--off-white); }

.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.0rem;
    font-weight: 700;
    color: var(--teal) !important;
    letter-spacing: 2.5px;
    border-bottom: 2px solid var(--teal);
    padding-bottom: 8px;
    margin-bottom: 18px;
    text-transform: uppercase;
}

/* ── Stat cards ── */
.stat-row { display: flex; gap: 14px; margin: 16px 0; flex-wrap: wrap; }
.stat-card {
    flex: 1; min-width: 120px;
    background: rgba(0,201,167,0.10);
    border: 1.5px solid var(--teal);
    border-radius: 14px;
    padding: 16px 12px;
    text-align: center;
    transition: transform 0.25s, box-shadow 0.25s;
}
.stat-card:hover { transform: translateY(-4px); box-shadow: 0 8px 28px var(--teal-glow); }
.stat-value {
    font-family: 'Orbitron', monospace;
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--teal) !important;
    text-shadow: 0 0 14px var(--teal-glow);
    line-height: 1.1;
}
.stat-label {
    font-size: 0.68rem;
    color: var(--muted) !important;
    margin-top: 6px;
    letter-spacing: 1.2px;
    font-weight: 600;
    text-transform: uppercase;
}

/* ── Main buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--teal), var(--teal-dark)) !important;
    color: #000000 !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    letter-spacing: 2px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 4px 18px rgba(0,201,167,0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.03) !important;
    box-shadow: 0 0 0 3px var(--teal), 0 8px 28px var(--teal-glow) !important;
}

/* ── Nav buttons ── */
.nav-btn > button {
    background: transparent !important;
    color: #ffffff !important;
    border: 1.5px solid rgba(255,255,255,0.25) !important;
    font-size: 0.72rem !important;
    padding: 7px 16px !important;
    box-shadow: none !important;
    letter-spacing: 1.5px !important;
}
.nav-btn > button:hover {
    border-color: var(--teal) !important;
    color: var(--teal) !important;
    box-shadow: 0 0 12px var(--teal-glow) !important;
    transform: translateY(-2px) !important;
}

/* ── ALL INPUT BOXES: white bg, black text, teal border ── */
input,
div[data-baseweb="input"] input,
.stNumberInput input,
.stTextInput input {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 2px solid var(--teal) !important;
    border-radius: 8px !important;
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.97rem !important;
    caret-color: #000000 !important;
}
input:focus,
div[data-baseweb="input"] input:focus,
.stNumberInput input:focus {
    background-color: #ffffff !important;
    color: #000000 !important;
    box-shadow: 0 0 0 3px var(--teal-glow) !important;
    outline: none !important;
}

/* ── Number input wrapper ── */
.stNumberInput > div > div {
    background: #ffffff !important;
    border: 2px solid var(--teal) !important;
    border-radius: 8px !important;
}
.stNumberInput button {
    background: rgba(0,201,167,0.12) !important;
    color: #000000 !important;
    border: none !important;
}

/* ── Multiselect: white bg, black text ── */
div[data-baseweb="select"] > div,
div[data-baseweb="select"] [role="combobox"] {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 2px solid var(--teal) !important;
    border-radius: 8px !important;
}
div[data-baseweb="select"] input {
    background-color: #ffffff !important;
    color: #000000 !important;
}
div[data-baseweb="tag"] {
    background-color: var(--teal) !important;
    color: #000000 !important;
    font-weight: 700 !important;
}
div[data-baseweb="select"] [role="option"] {
    background: #ffffff !important;
    color: #000000 !important;
    font-weight: 600 !important;
}
div[data-baseweb="select"] [role="option"]:hover {
    background: rgba(0,201,167,0.15) !important;
}
div[data-baseweb="popover"] {
    background: #ffffff !important;
    border: 2px solid var(--teal) !important;
    border-radius: 10px !important;
}

/* ── Labels above inputs — WHITE so visible on dark cards ── */
.stMultiSelect label,
.stNumberInput label,
.stSelectbox label,
.stTextInput label,
.stSlider label {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.5px !important;
}

/* ── Tip cards ── */
.tip-card {
    border-radius: 12px;
    padding: 14px 18px;
    margin: 10px 0;
    border-left: 5px solid;
    font-size: 0.93rem;
    line-height: 1.65;
    color: #ffffff !important;
    font-weight: 500;
}
.tip-card b  { color: #ffffff !important; font-weight: 800; }
.tip-1 { background: rgba(0,201,167,0.18);   border-color: var(--teal); }
.tip-2 { background: rgba(255,183,3,0.18);   border-color: var(--amber); }
.tip-3 { background: rgba(255,107,107,0.18); border-color: var(--coral); }

/* ── Hero ── */
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(1.9rem, 5vw, 3.3rem);
    font-weight: 900;
    color: #ffffff;
    line-height: 1.15;
    text-shadow: 0 0 40px var(--teal-glow);
    margin-bottom: 14px;
}
.hero-title .accent { color: var(--teal); }
.hero-sub {
    font-size: 1.02rem;
    color: rgba(255,255,255,0.78);
    max-width: 560px;
    line-height: 1.75;
}

/* ── Feature grid ── */
.feat-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; margin-top: 24px; }
.feat-item {
    background: rgba(10,28,48,0.75);
    border-radius: 14px;
    border: 1.5px solid rgba(0,201,167,0.35);
    padding: 22px 16px;
    text-align: center;
    transition: transform 0.25s, box-shadow 0.25s;
}
.feat-item:hover { transform: translateY(-6px); box-shadow: 0 12px 36px var(--teal-glow); }
.feat-icon  { font-family:'Orbitron',monospace; font-size:0.85rem; color:var(--teal) !important;
              font-weight:900; letter-spacing:2px; margin-bottom:10px; }
.feat-title { font-weight:700; font-size:0.90rem; color:#ffffff !important; margin-bottom:6px; }
.feat-desc  { font-size:0.78rem; color:rgba(255,255,255,0.65) !important; line-height:1.55; }

/* ── AI culprit badge ── */
.culprit-badge {
    background: rgba(255,107,107,0.14);
    border: 2px solid var(--coral);
    border-radius: 14px;
    padding: 16px 22px;
    margin: 14px 0;
    font-size: 0.97rem;
    font-weight: 600;
    color: #ffffff !important;
    line-height: 1.65;
}
.culprit-badge b    { color: #ffffff !important; font-weight: 800; }
.culprit-name       { color: #ff9a9a !important; font-size: 1.05rem; font-weight: 800; }

/* ── Appliance name box ── */
.app-name-box {
    display: flex;
    align-items: center;
    height: 50px;
    font-weight: 700;
    font-size: 0.92rem;
    color: #ffffff !important;
    background: rgba(0,201,167,0.10);
    border: 1.5px solid rgba(0,201,167,0.35);
    border-radius: 8px;
    padding: 0 14px;
}

/* ── Column header labels ── */
.col-header {
    font-family: 'Orbitron', monospace;
    font-size: 0.68rem;
    letter-spacing: 2px;
    font-weight: 700;
    padding: 2px 4px 8px;
    text-transform: uppercase;
}

/* ── Compare header ── */
.compare-header {
    font-family: 'Orbitron', monospace;
    font-size: 0.68rem;
    color: var(--teal) !important;
    letter-spacing: 2px;
    font-weight: 700;
    margin-bottom: 8px;
    text-transform: uppercase;
}

/* ── Dataframe overrides ── */
[data-testid="stDataFrame"] { background: transparent; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: rgba(0,0,0,0.3); }
::-webkit-scrollbar-thumb { background: var(--teal); border-radius: 6px; }

.js-plotly-plot .plotly,
.js-plotly-plot .plotly .main-svg { background: transparent !important; }
</style>
""", unsafe_allow_html=True)


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

c1, c2, c3, _sp = st.columns([1, 1, 1, 6])
with c1:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("HOME"):      nav_to("home")
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("CALCULATE"): nav_to("calculate")
    st.markdown('</div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("COMPARE"):   nav_to("compare")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")


# ══════════════════════════════════════════════════════════════════════════════
#  HOME
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:38px 0 22px 0;">
      <div class="hero-title">Smart Energy.<br><span class="accent">Zero Waste.</span><br>Lower Bills.</div>
      <div class="hero-sub">
        Track, analyse, and slash your electricity bills with India's most intelligent
        energy management platform — powered by real-time analytics and AI auditing.
      </div>
    </div>
    """, unsafe_allow_html=True)

    b1, b2 = st.columns([1, 1])
    with b1:
        if st.button("START CALCULATING"): nav_to("calculate")
    with b2:
        if st.button("COMPARE MONTHS"):    nav_to("compare")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-row">
      <div class="stat-card">
        <div class="stat-value">Rs 8.2K</div>
        <div class="stat-label">Avg Monthly Bill Saved</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">15+</div>
        <div class="stat-label">Appliances Tracked</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">AI</div>
        <div class="stat-label">Smart Audit Engine</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">Rs 6.5</div>
        <div class="stat-label">Per Unit Rate (kWh)</div>
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
        <div class="feat-desc">Plotly bar and area charts that grow on load for deep visual insights.</div>
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
        <div class="feat-desc">See your carbon footprint and how much CO2 you prevent each month.</div>
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
      <div class="section-title">Energy Calculator</div>
      <p style="color:rgba(255,255,255,0.80);font-weight:500;margin-bottom:0;">
        Select your appliances below. A daily-hours input appears instantly for each one.
        Your bill and CO2 footprint are computed in real time.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Appliance multiselect
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Select Appliances</div>', unsafe_allow_html=True)
    selected = st.multiselect(
        "Choose appliances used in your home:",
        list(APPLIANCES.keys()),
        key="calc_selected",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    hours_data: dict[str, float] = {}

    if selected:
        # ── Inline appliance + hours grid ─────────────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Daily Usage Hours</div>', unsafe_allow_html=True)
        st.markdown(
            '<p style="color:rgba(255,255,255,0.72);font-size:0.88rem;margin-bottom:14px;">'
            'Enter how many hours each appliance runs per day:</p>',
            unsafe_allow_html=True,
        )

        # Column headers
        h_app, h_hrs = st.columns([3, 2])
        with h_app:
            st.markdown('<div class="col-header" style="color:#00C9A7;">Appliance</div>',
                        unsafe_allow_html=True)
        with h_hrs:
            st.markdown('<div class="col-header" style="color:#00C9A7;">Hours / Day</div>',
                        unsafe_allow_html=True)

        for appliance in selected:
            col_app, col_hrs = st.columns([3, 2])
            with col_app:
                st.markdown(
                    f'<div class="app-name-box">{appliance}</div>',
                    unsafe_allow_html=True,
                )
            with col_hrs:
                h = st.number_input(
                    "hrs", min_value=0.0, max_value=24.0,
                    value=4.0, step=0.5,
                    key=f"calc_h_{appliance}",
                    label_visibility="collapsed",
                )
                hours_data[appliance] = h

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Calculations ──────────────────────────────────────────────────────
        days = 30
        rows = []
        for app, h in hours_data.items():
            w     = APPLIANCES[app]
            units = (w * h * days) / 1000
            cost  = units * RATE_PER_UNIT
            co2   = units * 0.82
            rows.append({
                "Appliance":   app,
                "Watts":       w,
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
            <div class="stat-label">Total Units (kWh)</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">Rs {total_cost:,.0f}</div>
            <div class="stat-label">Estimated Monthly Bill</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{total_co2:.1f} kg</div>
            <div class="stat-label">CO2 Footprint</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{len(selected)}</div>
            <div class="stat-label">Appliances Tracked</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Animated bar chart ────────────────────────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Cost Breakdown</div>', unsafe_allow_html=True)

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
            textfont=dict(color="#ffffff", size=11, family="Exo 2"),
            hovertemplate="<b>%{x}</b><br>Cost: Rs %{y:,.0f}<extra></extra>",
        ))
        fig_bar.frames = [
            go.Frame(data=[go.Bar(y=df["Cost (Rs)"] * (k / 20))], name=str(k))
            for k in range(1, 21)
        ]
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Exo 2", color="#ffffff"),
            xaxis=dict(
                tickangle=-35,
                tickfont=dict(size=11, color="#ffffff"),
                gridcolor="rgba(255,255,255,0.08)",
                linecolor="rgba(0,201,167,0.5)",
            ),
            yaxis=dict(
                title=dict(text="Rs Cost", font=dict(color="#ffffff")),
                tickfont=dict(color="#ffffff"),
                gridcolor="rgba(255,255,255,0.08)",
                linecolor="rgba(0,201,167,0.5)",
            ),
            margin=dict(t=50, b=100, l=70, r=20),
            updatemenus=[dict(
                type="buttons", showactive=False, y=1.12, x=0,
                buttons=[dict(
                    label="PLAY ANIMATION",
                    method="animate",
                    args=[None, {"frame": {"duration": 60, "redraw": True},
                                 "fromcurrent": True, "transition": {"duration": 30}}],
                )]
            )],
            height=420,
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Area chart ────────────────────────────────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Energy Units — Area View</div>', unsafe_allow_html=True)

        df_s = df.sort_values("Appliance")
        fig_area = go.Figure()
        fig_area.add_trace(go.Scatter(
            x=df_s["Appliance"], y=df_s["Units (kWh)"],
            name="Units (kWh)",
            fill="tozeroy", mode="lines+markers",
            line=dict(color="#00C9A7", width=3),
            fillcolor="rgba(0,201,167,0.18)",
            marker=dict(size=9, color="#00C9A7", line=dict(color="#fff", width=1.5)),
            hovertemplate="<b>%{x}</b><br>%{y:.2f} kWh<extra></extra>",
        ))
        fig_area.add_trace(go.Scatter(
            x=df_s["Appliance"], y=df_s["CO2 (kg)"],
            name="CO2 (kg)",
            fill="tozeroy", mode="lines+markers",
            line=dict(color="#FF6B6B", width=2.5, dash="dot"),
            fillcolor="rgba(255,107,107,0.12)",
            marker=dict(size=8, color="#FF6B6B"),
            hovertemplate="<b>%{x}</b><br>CO2: %{y:.2f} kg<extra></extra>",
        ))
        fig_area.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Exo 2", color="#ffffff"),
            xaxis=dict(tickangle=-35, tickfont=dict(color="#ffffff"),
                       gridcolor="rgba(255,255,255,0.08)"),
            yaxis=dict(tickfont=dict(color="#ffffff"), gridcolor="rgba(255,255,255,0.08)"),
            legend=dict(
                bgcolor="rgba(10,28,48,0.85)", bordercolor="#00C9A7",
                borderwidth=1, font=dict(color="#ffffff"),
            ),
            margin=dict(t=20, b=100, l=60, r=20), height=380,
        )
        st.plotly_chart(fig_area, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── AI Auditor ────────────────────────────────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">AI Energy Auditor Report</div>', unsafe_allow_html=True)

        culprit     = df.iloc[0]
        culprit_pct = (culprit["Cost (Rs)"] / total_cost * 100) if total_cost > 0 else 0
        watts       = APPLIANCES[culprit["Appliance"]]
        saving_1hr  = round((watts * 1 * 30 / 1000) * RATE_PER_UNIT, 0)

        st.markdown(f"""
        <div class="culprit-badge">
          CULPRIT APPLIANCE IDENTIFIED:
          <span class="culprit-name">&nbsp;{culprit["Appliance"]}</span><br><br>
          This appliance accounts for <b>{culprit_pct:.1f}%</b> of your total bill —
          costing <b>Rs {culprit["Cost (Rs)"]:,.0f} / month</b>
          at {culprit["Hours/Day"]} hrs/day.
        </div>
        """, unsafe_allow_html=True)

        tip1 = (f"Reduce <b>{culprit['Appliance']}</b> usage by 1 hr/day "
                f"and save <b>Rs {saving_1hr:,.0f}/month</b> immediately.")
        tip2 = ("Upgrade to a <b>5-star BEE-rated</b> model. "
                "Indian 5-star appliances use up to <b>40% less energy</b> than standard ones.")
        tip3 = ("Use a <b>smart plug timer</b> to cut standby power. "
                "Phantom drain silently adds <b>Rs 200–500/month</b> to your bill.")

        if watts >= 1000:
            tip2 = (f"Set a thermostat / schedule timer on your "
                    f"{culprit['Appliance'].split('(')[0].strip()}. "
                    f"Each degree of optimisation saves up to <b>Rs 350/month</b>.")
        if total_co2 > 50:
            tip3 = (f"Your footprint is <b>{total_co2:.1f} kg CO2/month</b>. "
                    f"A 1 kW rooftop solar panel offsets ~90 kg CO2 and cuts your bill by Rs 1,500+.")

        st.markdown(f"""
        <div class="tip-card tip-1"><b>TIP 1 — QUICK WIN:</b><br>{tip1}</div>
        <div class="tip-card tip-2"><b>TIP 2 — UPGRADE STRATEGY:</b><br>{tip2}</div>
        <div class="tip-card tip-3"><b>TIP 3 — SMART HABIT:</b><br>{tip3}</div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="compare-header">Detailed Breakdown Table</div>', unsafe_allow_html=True)
        st.dataframe(
            df[["Appliance", "Watts", "Hours/Day", "Units (kWh)", "Cost (Rs)", "CO2 (kg)"]],
            use_container_width=True, hide_index=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:52px 32px;">
          <div style="font-family:'Orbitron',monospace;font-size:1.5rem;
                      color:#00C9A7;letter-spacing:4px;margin-bottom:14px;">
            SELECT APPLIANCES ABOVE
          </div>
          <div style="color:rgba(255,255,255,0.72);font-size:0.97rem;line-height:1.75;">
            Choose one or more appliances from the list.<br>
            A daily-hours input will appear instantly for each one.
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
      <div class="section-title">Deep Comparison Mode</div>
      <p style="color:rgba(255,255,255,0.80);font-weight:500;margin-bottom:0;">
        Enter daily usage hours for <b style="color:#ffffff;">Last Month</b> and
        <b style="color:#ffffff;">This Month</b> for each appliance.
        The AI will identify what drove your bill up.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Select Appliances to Compare</div>', unsafe_allow_html=True)
    comp_selected = st.multiselect(
        "Choose appliances for month-on-month comparison:",
        list(APPLIANCES.keys()),
        key="comp_selected",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    last_hours: dict[str, float] = {}
    this_hours: dict[str, float] = {}

    if comp_selected:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Enter Hours Per Appliance</div>', unsafe_allow_html=True)

        # Column headers
        hdr_n, hdr_l, hdr_t = st.columns([3, 2, 2])
        with hdr_n:
            st.markdown('<div class="col-header" style="color:#00C9A7;">Appliance</div>',
                        unsafe_allow_html=True)
        with hdr_l:
            st.markdown('<div class="col-header" style="color:#4DAFFF;">Last Month (hrs/day)</div>',
                        unsafe_allow_html=True)
        with hdr_t:
            st.markdown('<div class="col-header" style="color:#00C9A7;">This Month (hrs/day)</div>',
                        unsafe_allow_html=True)

        for app in comp_selected:
            cn, cl, ct = st.columns([3, 2, 2])
            with cn:
                st.markdown(f'<div class="app-name-box">{app}</div>', unsafe_allow_html=True)
            with cl:
                lh = st.number_input(
                    "Last", min_value=0.0, max_value=24.0, value=4.0, step=0.5,
                    key=f"last_{app}", label_visibility="collapsed",
                )
                last_hours[app] = lh
            with ct:
                th = st.number_input(
                    "This", min_value=0.0, max_value=24.0, value=4.0, step=0.5,
                    key=f"this_{app}", label_visibility="collapsed",
                )
                this_hours[app] = th

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Build comparison df ───────────────────────────────────────────────
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

        cdf        = pd.DataFrame(cmp_rows).sort_values("Change (Rs)", ascending=False)
        total_last  = cdf["Last Month (Rs)"].sum()
        total_this  = cdf["This Month (Rs)"].sum()
        total_delta = total_this - total_last
        arrow       = "UP" if total_delta >= 0 else "DOWN"
        col_d       = "#ff7b7b" if total_delta >= 0 else "#00C9A7"

        st.markdown(f"""
        <div class="stat-row">
          <div class="stat-card">
            <div class="stat-value">Rs {total_last:,.0f}</div>
            <div class="stat-label">Last Month Total</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">Rs {total_this:,.0f}</div>
            <div class="stat-label">This Month Total</div>
          </div>
          <div class="stat-card">
            <div class="stat-value" style="color:{col_d};">{arrow} Rs {abs(total_delta):,.0f}</div>
            <div class="stat-label">Net Change</div>
          </div>
          <div class="stat-card">
            <div class="stat-value" style="color:{col_d};">
              {'+' if total_delta>=0 else ''}{(total_delta/total_last*100) if total_last else 0:.1f}%
            </div>
            <div class="stat-label">Percentage Change</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Grouped bar ───────────────────────────────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Side-by-Side Cost Comparison</div>', unsafe_allow_html=True)

        fig_grp = go.Figure()
        fig_grp.add_trace(go.Bar(
            name="Last Month", x=cdf["Appliance"], y=cdf["Last Month (Rs)"],
            marker_color="rgba(77,175,255,0.85)",
            marker_line=dict(color="#4DAFFF", width=1.5),
            text=[f"Rs {v:,.0f}" for v in cdf["Last Month (Rs)"]],
            textposition="outside", textfont=dict(color="#ffffff", size=10),
        ))
        fig_grp.add_trace(go.Bar(
            name="This Month", x=cdf["Appliance"], y=cdf["This Month (Rs)"],
            marker_color="rgba(0,201,167,0.85)",
            marker_line=dict(color="#00C9A7", width=1.5),
            text=[f"Rs {v:,.0f}" for v in cdf["This Month (Rs)"]],
            textposition="outside", textfont=dict(color="#ffffff", size=10),
        ))
        fig_grp.update_layout(
            barmode="group", bargap=0.22,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Exo 2", color="#ffffff"),
            xaxis=dict(tickangle=-35, tickfont=dict(color="#ffffff"),
                       gridcolor="rgba(255,255,255,0.07)"),
            yaxis=dict(
                tickfont=dict(color="#ffffff"),
                title=dict(text="Rs Cost", font=dict(color="#ffffff")),
                gridcolor="rgba(255,255,255,0.07)",
            ),
            legend=dict(
                bgcolor="rgba(10,28,48,0.85)", bordercolor="#00C9A7",
                borderwidth=1, font=dict(color="#ffffff"),
            ),
            margin=dict(t=30, b=100, l=60, r=20), height=420,
        )
        st.plotly_chart(fig_grp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Delta chart ───────────────────────────────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Change Analysis</div>', unsafe_allow_html=True)

        bar_cols = ["#ff7b7b" if v >= 0 else "#00C9A7" for v in cdf["Change (Rs)"]]
        fig_delta = go.Figure(go.Bar(
            x=cdf["Appliance"], y=cdf["Change (Rs)"],
            marker_color=bar_cols,
            marker_line=dict(color="rgba(255,255,255,0.25)", width=0.8),
            text=[f"{'+' if v>=0 else ''}Rs {v:,.0f}" for v in cdf["Change (Rs)"]],
            textposition="outside",
            textfont=dict(color="#ffffff", size=11, family="Exo 2"),
            hovertemplate="<b>%{x}</b><br>Change Rs %{y:,.0f}<extra></extra>",
        ))
        fig_delta.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.30)", line_width=1.5)
        fig_delta.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Exo 2", color="#ffffff"),
            xaxis=dict(tickangle=-35, tickfont=dict(color="#ffffff"),
                       gridcolor="rgba(255,255,255,0.07)"),
            yaxis=dict(
                tickfont=dict(color="#ffffff"),
                title=dict(text="Change (Rs)", font=dict(color="#ffffff")),
                gridcolor="rgba(255,255,255,0.07)", zeroline=False,
            ),
            margin=dict(t=30, b=100, l=60, r=20), height=380,
        )
        st.plotly_chart(fig_delta, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── AI Auditor ────────────────────────────────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">AI Auditor — Comparison Report</div>', unsafe_allow_html=True)

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
              Many Indian DISCOMs offer a <b>15–25% Time-of-Day discount</b> in night slots.
            </div>
            <div class="tip-card tip-3">
              <b>TIP 3 — SET A BUDGET ALERT:</b><br>
              Set a Rs {int(total_last * 1.05):,} monthly energy budget in your smart meter app.
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
        st.markdown('<div class="compare-header">Detailed Comparison Table</div>', unsafe_allow_html=True)
        st.dataframe(
            cdf[["Appliance", "Last Month (Rs)", "This Month (Rs)",
                 "Change (Rs)", "Last kWh", "This kWh"]],
            use_container_width=True, hide_index=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:52px 32px;">
          <div style="font-family:'Orbitron',monospace;font-size:1.5rem;
                      color:#00C9A7;letter-spacing:4px;margin-bottom:14px;">
            SELECT APPLIANCES ABOVE
          </div>
          <div style="color:rgba(255,255,255,0.72);font-size:0.97rem;line-height:1.75;">
            Choose appliances to begin your month-on-month comparison.<br>
            Side-by-side inputs, charts and AI report will appear instantly.
          </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;margin-top:48px;padding:20px;
            color:rgba(255,255,255,0.40);font-size:0.70rem;
            font-family:'Exo 2',sans-serif;letter-spacing:2px;">
  ECOWATT INDIA &nbsp;·&nbsp; PREMIUM ENERGY ANALYTICS &nbsp;·&nbsp;
  STREAMLIT + PLOTLY &nbsp;·&nbsp; RATE: RS 6.5 / kWh
</div>
""", unsafe_allow_html=True)
