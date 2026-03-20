import streamlit as st
import pandas as pd

st.set_page_config(page_title="EcoWatt India | Pro Audit", page_icon="⚡", layout="wide")

# Updated CSS for Maximum Readability
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.8), rgba(255,255,255,0.8)), 
                    url("https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 30px;
        border: 1px solid #d1d1d1;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .total-box {
        background: #1e293b;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        color: #00d1b2 !important;
        margin: 20px 0px;
    }
    .ai-box {
        background: #fff7ed;
        border-left: 5px solid #f97316;
        padding: 20px;
        border-radius: 8px;
        margin-top: 20px;
        color: #431407 !important;
    }
    /* Forcing all standard text to be dark for visibility */
    p, span, label, .stMarkdown {
        color: #1e293b !important;
        font-weight: 500;
    }
    h1, h2, h3 { 
        color: #0f172a !important; 
        font-weight: 700 !important;
    }
    .stButton>button {
        background-color: #0f172a;
        color: white !important;
        border-radius: 8px;
        height: 3.5em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #00d1b2;
        color: #0f172a !important;
    }
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
        st.title("⚡ ECOWATT INDIA")
        st.markdown("### Professional Energy Auditing & AI Analysis")
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("CALCULATE BILL"):
                st.session_state.page = 'calculate'
                st.rerun()
        with col2:
            if st.button("COMPARE USAGE"):
                st.session_state.page = 'compare'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'calculate':
    if st.button("⬅ BACK TO MENU"):
        st.session_state.page = 'home'
        st.rerun()
    
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.header("Appliance Consumption Audit")
        name = st.text_input("Enter Customer Name")
        
        if name:
            selected = st.multiselect("Select Household Appliances", list(app_lib.keys()))
            
            if selected:
                st.markdown("---")
                st.subheader("Set Daily Usage Hours")
                usage_data = {}
                cols = st.columns(3)
                for i, app in enumerate(selected):
                    with cols[i % 3]:
                        hr = st.number_input(f"{app} (Hrs)", 0.0, 24.0, 1.0, key=f"hr_{app}")
                        usage_data[app] = hr
                
                if st.button("GENERATE AI AUDIT"):
                    breakdown = []
                    for app, hrs in usage_data.items():
                        cost = app_lib[app] * hrs * 30 * 7.5
                        breakdown.append({"Appliance": app, "Hrs/Day": hrs, "Cost (INR)": round(cost, 2)})
                    
                    df = pd.DataFrame(breakdown)
                    total_bill = df["Cost (INR)"].sum()

                    st.markdown("---")
                    st.subheader(f"Detailed Analysis for {name}")
                    st.table(df)

                    st.markdown(f"""
                        <div class="total-box">
                            <p style="margin:0; font-size: 16px; color: white !important;">FINAL MONTHLY ESTIMATE</p>
                            <h1 style="margin:0; font-size: 48px; color: #00d1b2 !important;">INR {total_bill:,.2f}</h1>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown('<div class="ai-box">', unsafe_allow_html=True)
                    st.markdown("### 🤖 AI Improvement Strategy")
                    if total_bill > 2500:
                        st.markdown(f"**Action Required:** {name}, your bill is in the upper 20% tier.")
                        st.markdown("- **Peak Load:** Your heating/cooling devices are active for too long.")
                        st.markdown("- **Saving Tip:** Reducing AC by 90 mins daily saves ~INR 450/month.")
                    else:
                        st.markdown(f"**Status:** {name}, your consumption is efficient.")
                        st.markdown("- **Recommendation:** Continue using LED fixtures and 5-star appliances.")
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.area_chart(df.set_index("Appliance")["Cost (INR)"])
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'compare':
    if st.button("⬅ BACK TO MENU"):
        st.session_state.page = 'home'
        st.rerun()
    
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.header("Monthly Comparison")
        c1, c2 = st.columns(2)
        with c1:
            prev = st.number_input("Last Month (INR)", value=1500.0)
        with c2:
            curr = st.number_input("Current Month (INR)", value=1800.0)
        
        diff = curr - prev
        st.metric("Trend Analysis", f"INR {curr}", f"{((diff/prev)*100):.1f}%", delta_color="inverse")
        
        comp_df = pd.DataFrame({"Month": ["Previous", "Current"], "Bill": [prev, curr]})
        st.bar_chart(comp_df.set_index("Month"), color="#0f172a")
        st.markdown('</div>', unsafe_allow_html=True)
