import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


st.set_page_config(
    page_title="EcoWatt India",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APPLIANCES = {
    "LED Bulb (9W)":          9,
    "Tube Light (40W)":       40,
    "Ceiling Fan (75W)":      75,
    "AC 1.5 Ton (1500W)":    1500,
    "LED TV 32\" (60W)":      60,
    "Desktop PC (300W)":     300,
    "Laptop (65W)":           65,
    "Microwave (1200W)":      1200,
    " Electric Cooker (800W)": 800,
    " Electric Kettle (1500W)":1500,
    " Washing Machine (500W)": 500,
    " Refrigerator 300L (150W)":150,
    " Water Heater (2000W)":   2000,
    " Air Purifier (50W)":     50,
    "EV Charger (3300W)":     3300,
}

RATE_PER_UNIT = 6.5 
if "page" not in st.session_state:
    st.session_state.page = "home"
if "prev_page" not in st.session_state:
    st.session_state.prev_page = "home"

st.markdown("""
<style>
/* ===== Import Fonts ===== */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;700&display=swap');

/* ===== Root Variables ===== */
:root {
    --teal:      #00C9A7;
    --teal-glow: rgba(0,201,167,0.45);
    --teal-dark: #009e83;
    --amber:     #FFB703;
    --coral:     #FF6B6B;
    --bg-glass:  rgba(255,255,255,0.88);
    --black:     #000000;
    --dark:      #0a0a0a;
    --text:      #000000;
}


.stApp {
    background:
        linear-gradient(135deg, rgba(0,20,40,0.92) 0%, rgba(0,50,70,0.88) 100%),
        url("https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=1920&q=80")
        center/cover fixed no-repeat;
    font-family: 'Exo 2', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; }

.ecowatt-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-bottom: 2px solid var(--teal);
    border-radius: 0 0 18px 18px;
    padding: 14px 32px;
    margin-bottom: 28px;
    box-shadow: 0 4px 32px rgba(0,201,167,0.18);
    position: sticky;
    top: 0;
    z-index: 999;
}
.ecowatt-logo {
    font-family: 'Orbitron', monospace;
    font-size: 1.7rem;
    font-weight: 900;
    color: var(--teal);
    letter-spacing: 3px;
    text-shadow: 0 0 18px var(--teal-glow);
}
.ecowatt-logo span { color: #fff; }
.nav-tagline {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.6);
    letter-spacing: 2px;
    margin-top: -4px;
}


@keyframes slideInRight {
    from { opacity: 0; transform: translateX(60px); }
    to   { opacity: 1; transform: translateX(0); }
}
.page-wrapper {
    animation: slideInRight 0.45s cubic-bezier(0.25,0.8,0.25,1) both;
}


.glass-card {
    background: var(--bg-glass);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 20px;
    border: 1.5px solid rgba(0,201,167,0.35);
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.25), 0 0 0 1px rgba(255,255,255,0.1);
    color: var(--black) !important;
}
.glass-card h2, .glass-card h3, .glass-card p, .glass-card li {
    color: #000000 !important;
}

.stat-row { display: flex; gap: 18px; margin: 18px 0; }
.stat-card {
    flex: 1;
    background: linear-gradient(135deg, rgba(0,201,167,0.15), rgba(0,201,167,0.05));
    border: 2px solid var(--teal);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    transition: transform 0.25s, box-shadow 0.25s;
    backdrop-filter: blur(12px);
}
.stat-card:hover { transform: translateY(-5px); box-shadow: 0 8px 28px var(--teal-glow); }
.stat-value {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: var(--teal);
    text-shadow: 0 0 12px var(--teal-glow);
}
.stat-label { font-size: 0.82rem; color: rgba(255,255,255,0.75); margin-top: 4px; letter-spacing: 1px; }

.stButton > button {
    background: linear-gradient(135deg, var(--teal), var(--teal-dark)) !important;
    color: #000 !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 2px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 26px !important;
    transition: transform 0.2s, box-shadow 0.2s, border 0.2s !important;
    box-shadow: 0 4px 18px rgba(0,201,167,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.03) !important;
    box-shadow: 0 0 0 3px var(--teal), 0 8px 28px var(--teal-glow) !important;
}

.nav-btn > button {
    background: transparent !important;
    color: #fff !important;
    border: 1.5px solid rgba(255,255,255,0.25) !important;
    font-size: 0.75rem !important;
    padding: 7px 18px !important;
    box-shadow: none !important;
}
.nav-btn > button:hover {
    border: 1.5px solid var(--teal) !important;
    color: var(--teal) !important;
    box-shadow: 0 0 14px var(--teal-glow) !important;
    transform: translateY(-2px) !important;
}

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
    font-weight: 600 !important;
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

div[data-baseweb="select"] > div,
div[data-baseweb="select"] [role="combobox"],
div[data-baseweb="select"] div[role="listbox"] {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 2.5px solid var(--teal) !important;
    border-radius: 8px !important;
}
div[data-baseweb="tag"] {
    background-color: var(--teal) !important;
    color: #000 !important;
    font-weight: 700 !important;
}
div[data-baseweb="select"] [role="option"] {
    background: #fff !important;
    color: #000 !important;
}
div[data-baseweb="select"] [role="option"]:hover {
    background: rgba(0,201,167,0.15) !important;
}
div[data-baseweb="popover"] {
    background: #fff !important;
    border: 2px solid var(--teal) !important;
    border-radius: 10px !important;
}

.stNumberInput > div > div {
    background: #fff !important;
    border: 2.5px solid var(--teal) !important;
    border-radius: 8px !important;
}
    background: rgba(0,201,167,0.15) !important;
    color: #000 !important;
    border: none !important;
}

.stMultiSelect label, .stNumberInput label, .stSelectbox label, .stTextInput label,
.stSlider label {
    color: #000000 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.15rem;
    font-weight: 700;
    color: #000000;
    letter-spacing: 2px;
    border-bottom: 2px solid var(--teal);
    padding-bottom: 8px;
    margin-bottom: 18px;
}
.tip-card {
    border-radius: 12px;
    padding: 14px 18px;
    margin: 10px 0;
    border-left: 5px solid;
    font-weight: 700;
    font-size: 0.95rem;
    color: #000 !important;
}
.tip-1 { background: rgba(0,201,167,0.12); border-color: var(--teal); }
.tip-2 { background: rgba(255,183,3,0.12);  border-color: var(--amber); }
.tip-3 { background: rgba(255,107,107,0.12);border-color: var(--coral); }

.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 900;
    color: #ffffff;
    line-height: 1.15;
    text-shadow: 0 0 40px var(--teal-glow);
    margin-bottom: 12px;
}
.hero-title .accent { color: var(--teal); }
.hero-sub {
    font-size: 1.05rem;
    color: rgba(255,255,255,0.78);
    max-width: 560px;
    line-height: 1.7;
}

.feat-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 18px; margin-top: 24px; }
.feat-item {
    background: rgba(255,255,255,0.88);
    border-radius: 14px;
    border: 1.5px solid rgba(0,201,167,0.4);
    padding: 22px 18px;
    text-align: center;
    transition: transform 0.25s, box-shadow 0.25s;
    color: #000 !important;
}
.feat-item:hover { transform: translateY(-6px); box-shadow: 0 12px 36px var(--teal-glow); }
.feat-icon { font-size: 2.4rem; margin-bottom: 10px; }
.feat-title { font-weight: 700; font-size: 0.95rem; color: #000 !important; margin-bottom: 6px; }
.feat-desc  { font-size: 0.8rem; color: #333 !important; line-height: 1.5; }

.culprit-badge {
    background: linear-gradient(135deg, rgba(255,107,107,0.2), rgba(255,183,3,0.15));
    border: 2px solid var(--coral);
    border-radius: 14px;
    padding: 16px 22px;
    margin: 16px 0;
    font-size: 1rem;
    font-weight: 700;
    color: #000 !important;
}

.compare-header {
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    color: var(--teal);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); }
::-webkit-scrollbar-thumb { background: var(--teal); border-radius: 6px; }

.js-plotly-plot .plotly, .js-plotly-plot .plotly .main-svg { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

def nav_to(page: str):
    st.session_state.prev_page = st.session_state.page
    st.session_state.page = page



st.markdown("""
<div class="ecowatt-nav">
  <div>
    <div class="ecowatt-logo">⚡ EcoWatt<span> India</span></div>
    <div class="nav-tagline">PREMIUM ENERGY ANALYTICS PLATFORM</div>
  </div>
</div>
""", unsafe_allow_html=True)
col_n1, col_n2, col_n3, col_spacer = st.columns([1, 1, 1, 6])
with col_n1:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("🏠  HOME"):
        nav_to("home")
    st.markdown('</div>', unsafe_allow_html=True)
with col_n2:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("⚡  CALCULATE"):
        nav_to("calculate")
    st.markdown('</div>', unsafe_allow_html=True)
with col_n3:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("📊  COMPARE"):
        nav_to("compare")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("") 
if st.session_state.page == "home":
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)


    st.markdown("""
    <div style="padding: 40px 0 24px 0;">
      <div class="hero-title">Smart Energy.<br><span class="accent">Zero Waste.</span><br>Lower Bills.</div>
      <div class="hero-sub">
        Track, analyse, and slash your electricity bills with India's most intelligent
        energy management platform — powered by real-time analytics and AI auditing.
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("⚡  START CALCULATING  →"):
            nav_to("calculate")
    with c2:
        if st.button("📊  COMPARE MONTHS  →"):
            nav_to("compare")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-row">
      <div class="stat-card">
        <div class="stat-value">₹8.2K</div>
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
        <div class="stat-value">₹6.5</div>
        <div class="stat-label">PER UNIT RATE (kWh)</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="feat-grid">
      <div class="feat-item">
        <div class="feat-icon">⚡</div>
        <div class="feat-title">INSTANT CALCULATOR</div>
        <div class="feat-desc">Select appliances, enter daily hours — get your monthly bill in seconds.</div>
      </div>
      <div class="feat-item">
        <div class="feat-icon">📈</div>
        <div class="feat-title">ANIMATED CHARTS</div>
        <div class="feat-desc">Beautiful Plotly bar & area charts that grow on load for deep insights.</div>
      </div>
      <div class="feat-item">
        <div class="feat-icon">🤖</div>
        <div class="feat-title">AI AUDIT ENGINE</div>
        <div class="feat-desc">Identifies the "culprit" appliance and gives bold, actionable saving tips.</div>
      </div>
      <div class="feat-item">
        <div class="feat-icon">🔍</div>
        <div class="feat-title">DEEP COMPARISON</div>
        <div class="feat-desc">Side-by-side last vs this month comparison with change analysis.</div>
      </div>
      <div class="feat-item">
        <div class="feat-icon">🌿</div>
        <div class="feat-title">CO₂ TRACKER</div>
        <div class="feat-desc">See your carbon footprint and how much CO₂ you can prevent.</div>
      </div>
      <div class="feat-item">
        <div class="feat-icon">💎</div>
        <div class="feat-title">PREMIUM UI</div>
        <div class="feat-desc">Glassmorphism cards, slide transitions, and teal glow micro-interactions.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


elif st.session_state.page == "calculate":
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
      <div class="section-title">⚡ ENERGY CALCULATOR</div>
      <p style="color:#000;margin-bottom:0;">Select your appliances below and enter daily usage hours.
      Your bill and CO₂ footprint will be computed instantly.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔌 SELECT APPLIANCES</div>', unsafe_allow_html=True)
    selected = st.multiselect(
        "Choose appliances used in your home:",
        list(APPLIANCES.keys()),
        key="calc_selected",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    hours_data: dict[str, float] = {}

    if selected:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⏱️ DAILY USAGE HOURS</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, appliance in enumerate(selected):
            with cols[i % 3]:
                h = st.number_input(
                    f"{appliance}",
                    min_value=0.0,
                    max_value=24.0,
                    value=4.0,
                    step=0.5,
                    key=f"calc_h_{appliance}",
                )
                hours_data[appliance] = h
        st.markdown('</div>', unsafe_allow_html=True)
        days = 31
        rows = []
        for app, h in hours_data.items():
            watts = APPLIANCES[app]
            units = (watts * h * days) / 1000
            cost  = units * RATE_PER_UNIT
            co2   = units * 0.82  # kg CO₂ per kWh Indian grid
            rows.append({"Appliance": app, "Watts": watts, "Hours/Day": h,
                         "Units (kWh)": round(units, 2), "Cost (₹)": round(cost, 2),
                         "CO₂ (kg)": round(co2, 2)})

        df = pd.DataFrame(rows).sort_values("Cost (₹)", ascending=False)
        total_units = df["Units (kWh)"].sum()
        total_cost  = df["Cost (₹)"].sum()
        total_co2   = df["CO₂ (kg)"].sum()
        st.markdown(f"""
        <div class="stat-row">
          <div class="stat-card">
            <div class="stat-value">{total_units:.1f}</div>
            <div class="stat-label">TOTAL UNITS (kWh)</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">₹{total_cost:,.0f}</div>
            <div class="stat-label">ESTIMATED MONTHLY BILL</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{total_co2:.1f} kg</div>
            <div class="stat-label">CO₂ FOOTPRINT</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{len(selected)}</div>
            <div class="stat-label">APPLIANCES TRACKED</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 COST BREAKDOWN — ANIMATED</div>', unsafe_allow_html=True)

        colors = px.colors.sequential.Teal
        fig_bar = go.Figure()

        fig_bar.add_trace(go.Bar(
            x=df["Appliance"],
            y=df["Cost (₹)"],
            marker=dict(
                color=df["Cost (₹)"],
                colorscale="Teal",
                showscale=False,
                line=dict(color="#00C9A7", width=1.5),
            ),
            text=[f"₹{v:,.0f}" for v in df["Cost (₹)"]],
            textposition="outside",
            textfont=dict(color="#000", size=12, family="Exo 2"),
            hovertemplate="<b>%{x}</b><br>Cost: ₹%{y:,.0f}<extra></extra>",
        ))

        frames = [
            go.Frame(data=[go.Bar(y=df["Cost (₹)"] * (k / 20))], name=str(k))
            for k in range(1, 21)
        ]
        fig_bar.frames = frames

        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Exo 2", color="#000"),
            xaxis=dict(
                tickangle=-35,
                tickfont=dict(size=11, color="#000"),
                gridcolor="rgba(0,0,0,0.08)",
                linecolor="rgba(0,201,167,0.4)",
            ),
            yaxis=dict(
                title="₹ Cost",
                tickfont=dict(color="#000"),
                gridcolor="rgba(0,0,0,0.08)",
                linecolor="rgba(0,201,167,0.4)",
            ),
            margin=dict(t=20, b=80, l=60, r=20),
            updatemenus=[dict(
                type="buttons",
                showactive=False,
                y=1.1, x=0,
                buttons=[dict(
                    label="▶ PLAY",
                    method="animate",
                    args=[None, {"frame": {"duration": 60, "redraw": True},
                                 "fromcurrent": True, "transition": {"duration": 30}}]
                )]
            )],
            height=400,
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🌊 ENERGY UNITS — AREA VIEW</div>', unsafe_allow_html=True)

        fig_area = go.Figure()
        df_sorted = df.sort_values("Appliance")
        fig_area.add_trace(go.Scatter(
            x=df_sorted["Appliance"],
            y=df_sorted["Units (kWh)"],
            fill="tozeroy",
            mode="lines+markers",
            line=dict(color="#00C9A7", width=3),
            fillcolor="rgba(0,201,167,0.18)",
            marker=dict(size=10, color="#00C9A7", line=dict(color="#000", width=1.5)),
            hovertemplate="<b>%{x}</b><br>%{y:.2f} kWh<extra></extra>",
        ))
        fig_area.add_trace(go.Scatter(
            x=df_sorted["Appliance"],
            y=df_sorted["CO₂ (kg)"],
            fill="tozeroy",
            mode="lines+markers",
            name="CO₂ (kg)",
            line=dict(color="#FF6B6B", width=2.5, dash="dot"),
            fillcolor="rgba(255,107,107,0.10)",
            marker=dict(size=8, color="#FF6B6B"),
            hovertemplate="<b>%{x}</b><br>CO₂: %{y:.2f} kg<extra></extra>",
        ))
        fig_area.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Exo 2", color="#000"),
            xaxis=dict(tickangle=-35, tickfont=dict(color="#000"),
                       gridcolor="rgba(0,0,0,0.08)"),
            yaxis=dict(tickfont=dict(color="#000"), gridcolor="rgba(0,0,0,0.08)"),
            legend=dict(bgcolor="rgba(255,255,255,0.7)", bordercolor="#00C9A7",
                        borderwidth=1, font=dict(color="#000")),
            margin=dict(t=20, b=80, l=60, r=20),
            height=380,
        )
        st.plotly_chart(fig_area, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🤖 AI ENERGY AUDITOR REPORT</div>', unsafe_allow_html=True)

        culprit = df.iloc[0]
        culprit_pct = (culprit["Cost (₹)"] / total_cost * 100) if total_cost > 0 else 0
        watts = APPLIANCES[culprit["Appliance"]]

        st.markdown(f"""
        <div class="culprit-badge">
          🚨 CULPRIT APPLIANCE IDENTIFIED: <span style="color:#FF6B6B;">{culprit["Appliance"]}</span><br>
          This single appliance accounts for <b>{culprit_pct:.1f}%</b> of your total bill —
          costing you <b>₹{culprit["Cost (₹)"]:,.0f}/month</b> at {culprit["Hours/Day"]} hrs/day.
        </div>
        """, unsafe_allow_html=True)
        hours_culprit = culprit["Hours/Day"]
        saving_1hr    = round((watts * 1 * 30 / 1000) * RATE_PER_UNIT, 0)

        tip1 = f"Reduce <b>{culprit['Appliance']}</b> usage by just 1 hour/day → saves <b>₹{saving_1hr:,.0f}/month</b> instantly."
        tip2 = "Switch to a <b>5-star BEE rated</b> equivalent — Indian 5-star appliances use up to <b>40% less energy</b> than standard models."
        tip3 = "Use a <b>smart plug timer</b> to auto-cut power during off-peak hours — prevents phantom/standby drain that adds <b>₹200–₹500/month</b> silently."

        if watts >= 1000:
            tip2 = f"Set a <b>thermostat/temperature timer</b> on your {culprit['Appliance'].split('(')[0].strip()} — each degree optimisation saves up to <b>₹350/month</b>."
        if total_co2 > 50:
            tip3 = f"Your carbon footprint is <b>{total_co2:.1f} kg CO₂/month</b>. Installing <b>rooftop solar (1kW)</b> offsets ~90 kg CO₂ and cuts bills by ₹1,500+."

        st.markdown(f"""
        <div class="tip-card tip-1">💡 TIP 1 — QUICK WIN:<br>{tip1}</div>
        <div class="tip-card tip-2">⚙️ TIP 2 — UPGRADE STRATEGY:<br>{tip2}</div>
        <div class="tip-card tip-3">🌿 TIP 3 — SMART HABIT:<br>{tip3}</div>
        """, unsafe_allow_html=True)

        # Data table
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="compare-header">DETAILED BREAKDOWN TABLE</div>', unsafe_allow_html=True)
        st.dataframe(
            df[["Appliance", "Watts", "Hours/Day", "Units (kWh)", "Cost (₹)", "CO₂ (kg)"]],
            use_container_width=True,
            hide_index=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:48px;">
          <div style="font-size:3rem;">🔌</div>
          <div style="font-family:'Orbitron',monospace;font-size:1.1rem;color:#000;margin-top:12px;">
            Select appliances above to begin analysis
          </div>
          <div style="color:#333;margin-top:8px;">Your energy breakdown and AI report will appear here.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "compare":
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
      <div class="section-title">📊 DEEP COMPARISON MODE</div>
      <p style="color:#000;margin-bottom:0;">Enter daily usage hours for <b>Last Month</b> and <b>This Month</b>
      for each appliance. The AI will identify what drove your bill up.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔌 SELECT APPLIANCES TO COMPARE</div>', unsafe_allow_html=True)
    comp_selected = st.multiselect(
        "Choose appliances for month-on-month comparison:",
        list(APPLIANCES.keys()),
        key="comp_selected",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if comp_selected:
        last_hours: dict[str, float] = {}
        this_hours: dict[str, float] = {}

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col_last, col_this = st.columns(2)

        with col_last:
            st.markdown('<div class="compare-header">📅 LAST MONTH — DAILY HOURS</div>', unsafe_allow_html=True)
            for app in comp_selected:
                h = st.number_input(
                    f"{app}",
                    min_value=0.0, max_value=24.0, value=4.0, step=0.5,
                    key=f"last_{app}",
                )
                last_hours[app] = h

        with col_this:
            st.markdown('<div class="compare-header">📅 THIS MONTH — DAILY HOURS</div>', unsafe_allow_html=True)
            for app in comp_selected:
                h = st.number_input(
                    f"{app}",
                    min_value=0.0, max_value=24.0, value=4.0, step=0.5,
                    key=f"this_{app}",
                )
                this_hours[app] = h
        st.markdown('</div>', unsafe_allow_html=True)

        days = 30
        cmp_rows = []
        for app in comp_selected:
            w = APPLIANCES[app]
            lh, th = last_hours[app], this_hours[app]
            l_units = round((w * lh * days) / 1000, 2)
            t_units = round((w * th * days) / 1000, 2)
            l_cost  = round(l_units * RATE_PER_UNIT, 2)
            t_cost  = round(t_units * RATE_PER_UNIT, 2)
            delta   = round(t_cost - l_cost, 2)
            cmp_rows.append({
                "Appliance": app,
                "Last Month (₹)": l_cost,
                "This Month (₹)": t_cost,
                "Δ Change (₹)": delta,
                "Last kWh": l_units,
                "This kWh": t_units,
            })

        cdf = pd.DataFrame(cmp_rows).sort_values("Δ Change (₹)", ascending=False)
        total_last = cdf["Last Month (₹)"].sum()
        total_this = cdf["This Month (₹)"].sum()
        total_delta = total_this - total_last

        arrow = "🔺" if total_delta >= 0 else "🔻"
        color_delta = "#FF6B6B" if total_delta >= 0 else "#00C9A7"

        st.markdown(f"""
        <div class="stat-row">
          <div class="stat-card">
            <div class="stat-value">₹{total_last:,.0f}</div>
            <div class="stat-label">LAST MONTH TOTAL</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">₹{total_this:,.0f}</div>
            <div class="stat-label">THIS MONTH TOTAL</div>
          </div>
          <div class="stat-card">
            <div class="stat-value" style="color:{color_delta};">{arrow} ₹{abs(total_delta):,.0f}</div>
            <div class="stat-label">NET CHANGE</div>
          </div>
          <div class="stat-card">
            <div class="stat-value" style="color:{color_delta};">
              {'+' if total_delta>=0 else ''}{(total_delta/total_last*100) if total_last else 0:.1f}%
            </div>
            <div class="stat-label">PERCENTAGE CHANGE</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 SIDE-BY-SIDE COST COMPARISON</div>',
                    unsafe_allow_html=True)

        fig_grp = go.Figure()
        fig_grp.add_trace(go.Bar(
            name="Last Month",
            x=cdf["Appliance"],
            y=cdf["Last Month (₹)"],
            marker_color="rgba(100,180,255,0.85)",
            marker_line=dict(color="#4DAFFF", width=1.5),
            text=[f"₹{v:,.0f}" for v in cdf["Last Month (₹)"]],
            textposition="outside",
            textfont=dict(color="#000", size=10),
        ))
        fig_grp.add_trace(go.Bar(
            name="This Month",
            x=cdf["Appliance"],
            y=cdf["This Month (₹)"],
            marker_color="rgba(0,201,167,0.85)",
            marker_line=dict(color="#00C9A7", width=1.5),
            text=[f"₹{v:,.0f}" for v in cdf["This Month (₹)"]],
            textposition="outside",
            textfont=dict(color="#000", size=10),
        ))
        fig_grp.update_layout(
            barmode="group",
            bargap=0.22,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Exo 2", color="#000"),
            xaxis=dict(tickangle=-35, tickfont=dict(color="#000"),
                       gridcolor="rgba(0,0,0,0.06)"),
            yaxis=dict(tickfont=dict(color="#000"), title="₹ Cost",
                       gridcolor="rgba(0,0,0,0.06)"),
            legend=dict(bgcolor="rgba(255,255,255,0.7)", bordercolor="#00C9A7",
                        borderwidth=1, font=dict(color="#000")),
            margin=dict(t=30, b=90, l=60, r=20),
            height=420,
        )
        st.plotly_chart(fig_grp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Delta Waterfall ─────────────────────────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔺 CHANGE ANALYSIS — DELTA CHART</div>',
                    unsafe_allow_html=True)

        bar_colors = ["#FF6B6B" if v >= 0 else "#00C9A7" for v in cdf["Δ Change (₹)"]]
        fig_delta = go.Figure(go.Bar(
            x=cdf["Appliance"],
            y=cdf["Δ Change (₹)"],
            marker_color=bar_colors,
            marker_line=dict(color="#000", width=0.8),
            text=[f"{'+' if v>=0 else ''}₹{v:,.0f}" for v in cdf["Δ Change (₹)"]],
            textposition="outside",
            textfont=dict(color="#000", size=11, family="Exo 2"),
            hovertemplate="<b>%{x}</b><br>Δ ₹%{y:,.0f}<extra></extra>",
        ))
        fig_delta.add_hline(y=0, line_dash="dash", line_color="rgba(0,0,0,0.4)", line_width=1.5)
        fig_delta.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Exo 2", color="#000"),
            xaxis=dict(tickangle=-35, tickfont=dict(color="#000"),
                       gridcolor="rgba(0,0,0,0.06)"),
            yaxis=dict(tickfont=dict(color="#000"), title="Δ Cost (₹)",
                       gridcolor="rgba(0,0,0,0.06)", zeroline=False),
            margin=dict(t=30, b=90, l=60, r=20),
            height=380,
        )
        st.plotly_chart(fig_delta, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── AI Auditor for Comparison ───────────────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🤖 AI AUDITOR — COMPARISON REPORT</div>',
                    unsafe_allow_html=True)

        culprit_row = cdf[cdf["Δ Change (₹)"] > 0].iloc[0] if (cdf["Δ Change (₹)"] > 0).any() else None

        if culprit_row is not None:
            culprit_name = culprit_row["Appliance"]
            culprit_delta = culprit_row["Δ Change (₹)"]
            culprit_hrs_last = last_hours[culprit_name]
            culprit_hrs_this = this_hours[culprit_name]

            st.markdown(f"""
            <div class="culprit-badge">
              🚨 MONTH-ON-MONTH CULPRIT: <span style="color:#FF6B6B;">{culprit_name}</span><br>
              Usage increased from <b>{culprit_hrs_last} hrs/day → {culprit_hrs_this} hrs/day</b>,
              adding <b>₹{culprit_delta:,.0f}</b> to your bill this month.
            </div>

            <div class="tip-card tip-1">
              💡 <b>TIP 1 — REVERT USAGE:</b><br>
              Bring <b>{culprit_name}</b> back to {culprit_hrs_last} hrs/day and instantly
              recover <b>₹{culprit_delta:,.0f}/month</b>.
            </div>
            <div class="tip-card tip-2">
              ⚙️ <b>TIP 2 — SCHEDULE SMARTLY:</b><br>
              Use <b>off-peak hours (10 PM – 6 AM)</b> for high-wattage appliances.
              Many Indian DISCOMs offer <b>15–25% ToD discount</b> in night slots.
            </div>
            <div class="tip-card tip-3">
              🌿 <b>TIP 3 — SET A BUDGET ALERT:</b><br>
              Install a ₹{int(total_last * 1.05):,} monthly energy budget in a smart meter app —
              real-time alerts prevent bill shock before the cycle ends.
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="tip-card tip-1">
              <b>GREAT JOB!</b> Your usage did not increase for any appliance this month.
              Keep maintaining these habits to continue saving energy and money!
            </div>
            """, unsafe_allow_html=True)

        # Table
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="compare-header">DETAILED COMPARISON TABLE</div>', unsafe_allow_html=True)
        st.dataframe(
            cdf[["Appliance", "Last Month (₹)", "This Month (₹)", "Δ Change (₹)", "Last kWh", "This kWh"]],
            use_container_width=True,
            hide_index=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:48px;">
          <div style="font-size:3rem;">📊</div>
          <div style="font-family:'Orbitron',monospace;font-size:1.1rem;color:#000;margin-top:12px;">
            Select appliances above to start comparing months
          </div>
          <div style="color:#333;margin-top:8px;">Side-by-side charts and AI report will appear here.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;margin-top:48px;padding:20px;
            color:rgba(255,255,255,0.45);font-size:0.75rem;
            font-family:'Exo 2',sans-serif;letter-spacing:2px;">
  ⚡ ECOWATT INDIA &nbsp;·&nbsp; PREMIUM ENERGY ANALYTICS &nbsp;·&nbsp;
  BUILT WITH STREAMLIT + PLOTLY &nbsp;·&nbsp; RATE: ₹6.5/kWh
</div>
""", unsafe_allow_html=True)
