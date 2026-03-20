import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="EcoWatt India | Analytics", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1350&q=80");
        background-size: cover;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #00d1b2;
        color: white;
        font-weight: bold;
        border: none;
    }
    h1, h2, h3 { color: #00d1b2 !important; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.title("ECOWATT INDIA")
        st.write("Welcome to your Smart Energy Command Center. Please select an option to proceed.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Calculate This Month's Bill"):
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
    name = st.text_input("Customer Name")
    
    if name:
        app_lib = {"AC": 1.5, "Fridge": 0.25, "Fan": 0.07, "Lights": 0.05, "Geyser": 2.0}
        selected = st.multiselect("Select Appliances", list(app_lib.keys()))
        
        if selected:
            costs = []
            cols = st.columns(len(selected))
            for i, app in enumerate(selected):
                with cols[i]:
                    hrs = st.number_input(f"{app} (Hrs)", 0.0, 24.0, 1.0)
                    cost = hrs * app_lib[app] * 30 * 7.5
                    costs.append({"Appliance": app, "Cost": cost})
            
            df = pd.DataFrame(costs)
            total = df["Cost"].sum()
            
            st.metric("Estimated Bill", f"INR {total:,.2f}")
            st.area_chart(df.set_index("Appliance"), color="#00d1b2")

elif st.session_state.page == 'compare':
    if st.button("Back to Menu"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.header("Consumption Comparison")
    st.write("Compare your current usage with the previous month to find leaks.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        prev_bill = st.number_input("Last Month Total (INR)", value=1800.0)
    with col_b:
        curr_bill = st.number_input("This Month Total (INR)", value=2200.0)
    
    diff = curr_bill - prev_bill
    percent = (diff / prev_bill) * 100 if prev_bill != 0 else 0
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("Current vs Last Month", f"INR {curr_bill}", f"{percent:.1f}%", delta_color="inverse")
    
    comp_data = pd.DataFrame({
        "Month": ["Previous Month", "Current Month"],
        "Bill Amount (INR)": [prev_bill, curr_bill]
    })
    
    st.subheader("Financial Trend")
    st.bar_chart(comp_data.set_index("Month"), color="#ff9933" if diff > 0 else "#00d1b2")
    
    if diff > 0:
        st.error(f"Your bill increased by INR {diff:.2f}. Check your high-wattage appliance logs.")
    else:
        st.success(f"Great! You saved INR {abs(diff):.2f} compared to last month.")
    st.markdown('</div>', unsafe_allow_html=True)
