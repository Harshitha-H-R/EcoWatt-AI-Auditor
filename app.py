import streamlit as st
import pandas as pd

st.set_page_config(page_title="EcoWatt India | Analytics", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url("https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=1350&q=80");
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
    .total-box {
        background: rgba(0, 209, 178, 0.2);
        border: 2px solid #00d1b2;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-top: 20px;
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

app_lib = {
    "Refrigerator": 0.25, "Washing Machine": 0.5, "Dishwasher": 1.5,
    "Air Conditioner": 1.5, "Electric Oven": 2.0, "Clothes Dryer": 3.0,
    "Microwave Oven": 1.0, "Vacuum Cleaner": 0.8, "Electric Iron": 1.1,
    "Blender/Mixer": 0.4, "Coffee Maker": 0.8, "Television": 0.1,
    "Computer/Desktop": 0.2, "Hair Dryer": 1.5, "Electric Fan": 0.07,
    "Electric Kettle": 1.5, "Toaster": 0.8
}

if st.session_state.page == 'home':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="main-card" style="text-align: center;">', unsafe_allow_html=True)
        st.title("ECOWATT INDIA")
        st.write("Professional Home Energy Auditing System")
        st.markdown("<br>", unsafe_allow_html=True)
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
    
    st.header("Appliance Consumption Audit")
    name = st.text_input("Enter Customer Name")
    
    if name:
        selected = st.multiselect("Step 1: Select Appliances", list(app_lib.keys()))
        
        if selected:
            st.markdown("### Step 2: Enter Daily Usage Hours")
            usage_data = {}
            # Display inputs in a clean 3-column grid
            cols = st.columns(3)
            for i, app in enumerate(selected):
                with cols[i % 3]:
                    hr = st.number_input(f"Hours for {app}", 0.0, 24.0, 1.0, key=f"hr_{app}")
                    usage_data[app] = hr
            
            # Auto-calculate and show breakdown table
            breakdown = []
            for app, hrs in usage_data.items():
                cost = app_lib[app] * hrs * 30 * 7.5
                breakdown.append({"Appliance": app, "Daily Hrs": hrs, "Monthly Cost (INR)": round(cost, 2)})
            
            df = pd.DataFrame(breakdown)
            total_bill = df["Monthly Cost (INR)"].sum()

            st.markdown("---")
            st.subheader("Analysis Results")
            st.table(df)

            # High-impact total box
            st.markdown(f"""
                <div class="total-box">
                    <h2 style="margin:0; color:white !important;">Total Monthly Estimate</h2>
                    <h1 style="margin:0; font-size: 50px; color:#00d1b2 !important;">INR {total_bill:,.2f}</h1>
                </div>
            """, unsafe_allow_html=True)
            
            st.area_chart(df.set_index("Appliance")["Monthly Cost (INR)"], color="#00d1b2")

elif st.session_state.page == 'compare':
    if st.button("Back to Menu"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.header("Monthly Comparison")
    c1, c2 = st.columns(2)
    with c1:
        prev = st.number_input("Last Month (INR)", value=1500.0)
    with c2:
        curr = st.number_input("Current Month (INR)", value=1800.0)
    
    diff = curr - prev
    percent = (diff / prev * 100) if prev != 0 else 0
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.metric("Bill Difference", f"INR {curr}", f"{percent:.1f}%", delta_color="inverse")
    comp_df = pd.DataFrame({"Month": ["Previous", "Current"], "Bill": [prev, curr]})
    st.bar_chart(comp_df.set_index("Month"), color="#00d1b2")
    st.markdown('</div>', unsafe_allow_html=True)
