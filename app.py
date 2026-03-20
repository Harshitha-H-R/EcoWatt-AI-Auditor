import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="EcoWatt India",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

RATE_PER_UNIT = 6.5
DAYS_IN_MONTH = 30
CO2_FACTOR = 0.82

APPLIANCES = {
    "LED Bulb (9W)": 9,
    "Tube Light (40W)": 40,
    "Ceiling Fan (75W)": 75,
    "AC 1.5 Ton (1500W)": 1500,
    "LED TV 32in (60W)": 60,
    "Desktop PC (300W)": 300,
    "Laptop (65W)": 65,
    "Microwave (1200W)": 1200,
    "Electric Cooker (800W)": 800,
    "Electric Kettle (1500W)": 1500,
    "Washing Machine (500W)": 500,
    "Refrigerator 300L (150W)": 150,
    "Water Heater (2000W)": 2000,
    "Air Purifier (50W)": 50,
    "EV Charger (3300W)": 3300,
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;700&display=swap');
:root {
    --teal: #00C9A7; --teal-glow: rgba(0,201,167,0.5); --teal-dark: #009e83;
    --amber: #FFB703; --coral: #FF6B6B; --white: #ffffff; --card-bg: rgba(10,28,48,0.78);
}
.stApp {
    background: linear-gradient(135deg, rgba(0,12,28,0.96) 0%, rgba(0,35,55,0.94) 100%),
    url("https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=1920&q=80") center/cover fixed no-repeat;
    font-family: 'Exo 2', sans-serif; color: var(--white);
}
#MainMenu, footer, header { visibility: hidden; }
.ecowatt-nav {
    display: flex; align-items: center; background: rgba(0,0,0,0.70); backdrop-filter: blur(20px);
    border-bottom: 2px solid var(--teal); border-radius: 0 0 16px 16px; padding: 14px 32px;
    margin-bottom: 24px; box-shadow: 0 4px 32px rgba(0,201,167,0.20);
}
.ecowatt-logo { font-family: 'Orbitron', monospace; font-size: 1.65rem; font-weight: 900; color: var(--teal); letter-spacing: 3px; }
.glass-card { background: var(--card-bg); border-radius: 18px; border: 1.5px solid rgba(0,201,167,0.35); padding: 26px 30px; margin-bottom: 20px; }
.section-title { font-family: 'Orbitron', monospace; font-size: 1.0rem; color: var(--teal) !important; border-bottom: 2px solid var(--teal); padding-bottom: 8px; margin-bottom: 18px; }
.stat-card { flex: 1; background: rgba(0,201,167,0.10); border: 1.5px solid var(--teal); border-radius: 14px; padding: 16px 12px; text-align: center; }
.stat-value { font-family: 'Orbitron', monospace; font-size: 1.7rem; color: var(--teal) !important; }
.stButton > button { background: linear-gradient(135deg, var(--teal), var(--teal-dark)) !important; color: #000!important; font-family: 'Orbitron'!important; font-weight: 700!important; border-radius: 10px!important; }
input, div[data-baseweb="input"] input { background-color: #fff!important; color: #000!important; border: 2px solid var(--teal)!important; border-radius: 8px!important; font-weight: 700!important; }
.tip-card { border-radius: 12px; padding: 14px 18px; margin: 10px 0; border-left: 5px solid; color: #fff!important; }
.tip-1 { background: rgba(0,201,167,0.18); border-color: var(--teal); }
.culprit-badge { background: rgba(255,107,107,0.14); border: 2px solid var(--coral); border-radius: 14px; padding: 16px 22px; margin: 14px 0; }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

def navigate(page: str):
    st.session_state.page = page

st.markdown("""
<div class="ecowatt-nav">
  <div>
    <div class="ecowatt-logo">EcoWatt<span> India</span></div>
    <div style="font-size:0.7rem; color:rgba(255,255,255,0.6); letter-spacing:2px;">PREMIUM ANALYTICS</div>
  </div>
</div>
""", unsafe_allow_html=True)

nav_cols = st.columns([1, 1, 1, 6])
with nav_cols[0]:
    if st.button("HOME", use_container_width=True): navigate("home")
with nav_cols[1]:
    if st.button("CALCULATE", use_container_width=True): navigate("calculate")
with nav_cols[2]:
    if st.button("COMPARE", use_container_width=True): navigate("compare")

if st.session_state.page == "home":
    st.markdown('<div class="hero-title" style="font-family:Orbitron; font-size:3rem; font-weight:900; margin:40px 0;">Smart Energy.<br><span style="color:#00C9A7">Zero Waste.</span></div>', unsafe_allow_html=True)
    st.write("Track, analyse, and slash your electricity bills with India's most intelligent energy management platform.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("START CALCULATING", use_container_width=True): navigate("calculate")
    with col_b:
        if st.button("COMPARE MONTHS", use_container_width=True): navigate("compare")

elif st.session_state.page == "calculate":
    st.markdown('<div class="glass-card"><div class="section-title">Energy Audit</div></div>', unsafe_allow_html=True)
    selected = st.multiselect("Select appliances used in your home:", list(APPLIANCES.keys()))
    
    if selected:
        hours_data = {}
        st.markdown('<div class="glass-card"><div class="section-title">Usage Hours</div>', unsafe_allow_html=True)
        for app in selected:
            col_l, col_r = st.columns([3, 1])
            col_l.markdown(f'<div style="padding:10px; background:rgba(0,201,167,0.1); border-radius:8px; margin-bottom:5px;">{app}</div>', unsafe_allow_html=True)
            hours_data[app] = col_r.number_input("Hrs", 0.0, 24.0, 4.0, 0.5, key=f"calc_{app}", label_visibility="collapsed")
        
        results = []
        for app, h in hours_data.items():
            units = (APPLIANCES[app] * h * DAYS_IN_MONTH) / 1000
            results.append({
                "Appliance": app, 
                "Units (kWh)": units, 
                "Cost (Rs)": units * RATE_PER_UNIT,
                "CO2 (kg)": units * CO2_FACTOR
            })
        
        df = pd.DataFrame(results).sort_values("Cost (Rs)", ascending=False)
        
        st.columns(4)[0].metric("Total Units", f"{df['Units (kWh)'].sum():.1f} kWh")
        st.columns(4)[1].metric("Monthly Bill", f"Rs {df['Cost (Rs)'].sum():,.0f}")
        
        fig = go.Figure(go.Bar(x=df["Appliance"], y=df["Cost (Rs)"], marker_color="#00C9A7"))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

elif st.session_state.page == "compare":
    st.markdown('<div class="glass-card"><div class="section-title">Comparative Analytics</div></div>', unsafe_allow_html=True)
    comp_selected = st.multiselect("Choose appliances to compare:", list(APPLIANCES.keys()))
    
    if comp_selected:
        comp_data = []
        for app in comp_selected:
            c1, c2, c3 = st.columns([2, 1, 1])
            c1.write(f"**{app}**")
            lh = c2.number_input("Last Month", 0.0, 24.0, 4.0, key=f"l_{app}")
            th = c3.number_input("This Month", 0.0, 24.0, 4.0, key=f"t_{app}")
            
            l_cost = (APPLIANCES[app] * lh * DAYS_IN_MONTH / 1000) * RATE_PER_UNIT
            t_cost = (APPLIANCES[app] * th * DAYS_IN_MONTH / 1000) * RATE_PER_UNIT
            comp_data.append({"Appliance": app, "Last Month": l_cost, "This Month": t_cost})
        
        cdf = pd.DataFrame(comp_data)
        st.bar_chart(cdf.set_index("Appliance"))
        
        diff = cdf["This Month"].sum() - cdf["Last Month"].sum()
        if diff > 0:
            st.error(f"Bill Increased by Rs {diff:,.2f}")
        else:
            st.success(f"Bill Decreased by Rs {abs(diff):,.2f}")
