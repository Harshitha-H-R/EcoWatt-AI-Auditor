import streamlit as st
import pandas as pd
import time 
st.set_page_config(page_title="EcoWatt India Pro", page_icon="⚡", layout="wide")
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80");
        background-size: cover;
        color: white;
    }
    .report-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 20px;
    }
    h1, h2, h3, p { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("EcoWatt AI: Smart Auditor")
user_name = st.text_input("May I know your Good Name:", placeholder="e.g., Harsh")

if user_name:
    st.markdown("### Select your Appliances")
    appliance_dict = {
        "AC (1.5 Ton)": 1.5, "Fridge": 0.2, "Ceiling Fan": 0.07, 
        "LED Lights": 0.05, "Geyser": 2.0, "Laptop": 0.1
    }
    
    selected = st.multiselect("Pick appliances used today:", list(appliance_dict.keys()))

    if selected:
        usage_hours = {}
        st.write("---")
        cols = st.columns(len(selected))
        for i, app in enumerate(selected):
            with cols[i]:
                usage_hours[app] = st.number_input(f"{app} (Hrs)", 0, 24, 1)

        if st.button(" GENERATE AI AUDIT"):
            with st.status("🤖 AI is analyzing your load profile...", expanded=True) as status:
                st.write("Calculating kWh consumption...")
                time.sleep(1)
                st.write("Applying Indian Tariff rates (₹7/unit)...")
                time.sleep(1)
                st.write("Generating optimization remarks...")
                time.sleep(1)
                status.update(label=" Audit Complete!", state="complete", expanded=False)
            total_kwh = sum(appliance_dict[app] * hrs for app, hrs in usage_hours.items())
            monthly_bill = total_kwh * 30 * 7.0
            st.markdown(f'<div class="report-card">', unsafe_allow_html=True)
            st.header(f"Report for {user_name}")
            c1, c2 = st.columns(2)
            c1.metric("Daily Consumption", f"{total_kwh:.2f} kWh")
            c2.metric("Est. Monthly Bill", f"₹{monthly_bill:,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="report-card" style="border-left: 5px solid #ff9933;">', unsafe_allow_html=True)
            st.subheader(" AI Optimization Strategy")
            if monthly_bill > 1500:
                st.error(f"High usage detected! {user_name}, reducing AC by 2 hours can save ₹600/month.")
            else:
                st.success("Your energy footprint is efficient. Keep it up!")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.bar_chart(pd.DataFrame({"App": list(usage_hours.keys()), "kWh": [appliance_dict[a]*usage_hours[a] for a in usage_hours]}).set_index("App"))
