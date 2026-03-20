import streamlit as st
import pandas as pd

st.set_page_config(page_title="EcoWatt India", page_icon="⚡", layout="wide")

# Custom CSS for Indian Branding
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { background-color: #ff9933; color: white; border-radius: 8px; }
    .report-box { padding: 20px; border-radius: 10px; background-color: white; border-left: 10px solid #138808; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ EcoWatt AI: Personal Energy Auditor")
st.write("---")

# 2. Step 1: User Identity
user_name = st.text_input("May I know your Good Name :", placeholder="e.g., Harsh")

if user_name:
    st.success(f"Welcome, {user_name}! Let's analyze your household energy.")

    # 3. Step 2: Appliance Selection
    st.subheader("Step 2: Select your Appliances")
    appliance_list = {
        "Air Conditioner (1.5 Ton)": 1.5,
        "Refrigerator": 0.2,
        "Ceiling Fan": 0.075,
        "LED Bulbs (Set of 5)": 0.05,
        "Geyser/Water Heater": 2.0,
        "Washing Machine": 0.5,
        "Laptop/PC": 0.1
    }
    
    selected = st.multiselect("Which appliances did you use today?", list(appliance_list.keys()))

    # 4. Step 3: Hour Inputs
    if selected:
        st.subheader("Step 3: Total Usage Hours")
        usage_data = {}
        cols = st.columns(len(selected))
        
        for i, app in enumerate(selected):
            with cols[i % len(cols)]:
                hours = st.number_input(f"Hours for {app}", 0, 24, 1, key=app)
                usage_data[app] = hours

        # 5. Step 4: Cost Configuration (Indian Context)
        st.sidebar.header(" Billing Settings")
        rate_per_unit = st.sidebar.number_input("Rate per Unit (₹)", value=7.0)

        # 6. Step 5: Calculations
        total_kwh = 0
        for app, hrs in usage_data.items():
            total_kwh += appliance_list[app] * hrs
        
        daily_cost = total_kwh * rate_per_unit
        monthly_cost = daily_cost * 30

        # 7. Final Report Display
        st.write("---")
        st.markdown(f"### Energy Report for {user_name}")
        
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric("Total Daily Consumption", f"{total_kwh:.2f} kWh")
        with m_col2:
            st.metric("Estimated Monthly Bill", f"₹{monthly_cost:,.2f}")

        # AI Remarks Logic
        st.subheader("AI Auditor Remarks")
        
        with st.container():
            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            if monthly_cost > 3000:
                st.error(f"**Critical Remark:** {user_name}, your usage is very high for an Indian household. Your heavy appliances (AC/Geyser) are causing a massive spike. Switch to 'Star Rated' appliances to save nearly ₹800/month.")
            elif 1000 <= monthly_cost <= 3000:
                st.warning(f"**Moderate Remark:** Good usage, {user_name}. However, your standby loads (like the Refrigerator or PC) are consistent. Unplugging devices when not in use can shave 5% off your ₹{monthly_cost:.0f} bill.")
            else:
                st.success(f"**Excellent Remark:** Outstanding energy management, {user_name}! You are well within the green zone. Consider installing a small 1kW Solar Rooftop to bring this bill to zero.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Visualization
        st.write("###  Consumption Breakdown")
        chart_df = pd.DataFrame({
            "Appliance": list(usage_data.keys()),
            "kWh": [appliance_list[app] * usage_data[app] for app in usage_data.keys()]
        })
        st.bar_chart(chart_df.set_index("Appliance"))

else:
    st.info("Please enter your name above to unlock the auditor.")