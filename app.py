import streamlit as st
import pandas as pd

st.set_page_config(page_title="EcoWatt India | Analytics", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url("https://images.unsplash.com/photo-1556911220-e15024d8393e?auto=format&fit=crop&w=1350&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #00d1b2;
        color: white;
        font-weight: bold;
    }
    h1, h2, h3 { color: #00d1b2 !important; }
    label { color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Organized Appliance Dictionary (kW ratings)
app_lib = {
    "Major Appliances": {
        "Refrigerator": 0.25, "Washing Machine": 0.5, "Dishwasher": 1.5,
        "Air Conditioner": 1.5, "Electric Oven": 2.0, "Clothes Dryer": 3.0
    },
    "Small Appliances": {
        "Microwave Oven": 1.0, "Vacuum Cleaner": 0.8, "Electric Iron": 1.1,
        "Blender/Mixer": 0.4, "Coffee Maker": 0.8, "Toaster": 0.8, "Electric Kettle": 1.5
    },
    "Electronics": {
        "Television": 0.1, "Computer/Desktop": 0.2, "Hair Dryer": 1.5, "Electric Fan": 0.07
    }
}

# Flatten for calculations
flat_apps = {**app_lib["Major Appliances"], **app_lib["Small Appliances"], **app_lib["Electronics"]}

if st.session_state.page == 'home':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="main-card" style="text-align: center;">', unsafe_allow_html=True)
        st.title("ECOWATT INDIA")
        st.write("Smart Energy Command Center")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Calculate Monthly Bill"):
                st.session_state.page = 'calculate'
                st.rerun()
        with col2:
            if st.button("Compare Monthly Usage"):
                st.session_state.page = 'compare'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'calculate':
    if st.button("Back to Menu"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.header("Monthly Bill Audit")
    name = st.text_input("Enter Customer Name")
    
    if name:
        selected = st.multiselect("Select your appliances:", list(flat_apps.keys()))
        
        if selected:
            st.write("---")
            st.subheader("Set Daily Usage Hours")
            
            # This is where it asks for EACH appliance input
            usage_data = {}
            cols = st.columns(3) # 3 columns to keep it clean
            for i, app in enumerate(selected):
                with cols[i % 3]:
                    # Dynamic unique key for each input
                    hr = st.number_input(f"Hours for {app}", 0.0, 24.0, 1.0, key=f"hr_{app}")
                    usage_data[app] = hr

            if st.button("Generate Detailed Report"):
                costs = []
                for app, hrs in usage_data.items():
                    # Formula: kW * Hours * 30 days * 7.5 INR rate
                    m_cost = flat_apps[app] * hrs * 30 * 7.5
                    costs.append({"Appliance": app, "Cost (INR)": round(m_cost, 2)})
                
                df = pd.DataFrame(costs)
                total = df["Cost (INR)"].sum()
                
                st.markdown('<div class="main-card">', unsafe_allow_html=True)
                st.subheader(f"Results for {name}")
                st.metric("Total Monthly Estimate", f"INR {total:,.2f}")
                
                # Elegant Chart
                st.area_chart(df.set_index("Appliance"), color="#00d1b2")
                
                # Detailed Breakdown Table
                st.table(df)
                st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'compare':
    if st.button("Back to Menu"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.header("Comparison Analysis")
    c1, c2 = st.columns(2)
    with c1:
        prev = st.number_input("Last Month (INR)", 0.0, 50000.0, 1500.0)
    with c2:
        curr = st.number_input("Current Month (INR)", 0.0, 50000.0, 1800.0)
    
    diff = curr - prev
    percent = (diff / prev * 100) if prev != 0 else 0
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.metric("Bill Difference", f"INR {curr}", f"{percent:.1f}%", delta_color="inverse")
    

    comp_df = pd.DataFrame({"Month": ["Previous", "Current"], "Bill": [prev, curr]})
    st.bar_chart(comp_df.set_index("Month"), color="#00d1b2")

    if diff > 1000:
        st.error(f"Alert: Increase of INR {diff:.2f}. Major load reduction required.")
    elif diff > 500:
        st.warning(f"Note: Increase of INR {diff:.2f}. Check high-wattage devices.")
    elif diff < 0:
        st.success(f"Savings of INR {abs(diff):.2f} achieved!")
    st.markdown('</div>', unsafe_allow_html=True)
