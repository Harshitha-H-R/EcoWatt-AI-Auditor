import streamlit as st
import pandas as pd

st.set_page_config(page_title="EcoWatt India | Analytics", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* 1. RESTORED THE GOOD BACKGROUND */
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), 
                    url("https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-attachment: fixed;
    }

    /* 2. SYNCED BOXES: Normal state AND Clicking (Focus) state */
    /* This forces the box to be white and text to be black ALWAYS */
    input, div[data-baseweb="input"], div[data-baseweb="select"], .stNumberInput div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #00d1b2 !important;
        border-radius: 8px !important;
    }
    
    /* This handles the 'Click' (Focus) color specifically */
    input:focus, div[data-baseweb="input"]:focus-within {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #0f172a !important;
        box-shadow: 0 0 0 2px rgba(0,209,178,0.2) !important;
    }

    /* 3. FORCE BLACK TEXT FOR ALL LABELS & HEADERS */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #000000 !important;
        font-weight: 700 !important;
    }

    /* 4. Card Styling */
    .main-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 30px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }

    .report-box {
        background: #f1f5f9;
        border-left: 10px solid #00d1b2;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        color: #000000 !important;
    }

    /* 5. Buttons */
    .stButton>button {
        background-color: #0f172a;
        color: #FFFFFF !important;
        border-radius: 8px;
        font-weight: bold;
        height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'home'

app_lib = {
    "Refrigerator": 0.25, "Washing Machine": 0.5, "Dishwasher": 1.5,
    "Air Conditioner": 1.5, "Electric Oven": 2.0, "Microwave Oven": 1.0,
    "Vacuum Cleaner": 0.8, "Electric Iron": 1.1, "Television": 0.1,
    "Computer": 0.2, "Hair Dryer": 1.5, "Electric Fan": 0.07,
    "Electric Kettle": 1.5, "Toaster": 0.8
}

if st.session_state.page == 'home':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="main-card" style="text-align: center;">', unsafe_allow_html=True)
        st.title("⚡ ECOWATT INDIA")
        st.markdown("### Professional Energy Auditing & Comparative Analytics")
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("CALCULATE BILL"):
                st.session_state.page = 'calculate'
                st.rerun()
        with col2:
            if st.button("COMPARE MONTHS"):
                st.session_state.page = 'compare'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'calculate':
    if st.button("⬅ MENU"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.header("Appliance Consumption Audit")
    name = st.text_input("Enter Customer Name", key="name_box")
    
    if name:
        selected = st.multiselect("Select Appliances", list(app_lib.keys()))
        if selected:
            st.markdown("---")
            st.subheader("Daily Usage (Hours)")
            usage_data = {}
            cols = st.columns(3)
            for i, app in enumerate(selected):
                with cols[i % 3]:
                    hr = st.number_input(f"{app}", 0.0, 24.0, 1.0, key=f"c_{app}")
                    usage_data[app] = hr
            
            if st.button("GENERATE REPORT"):
                breakdown = [{"Appliance": a, "Cost (INR)": round(app_lib[a]*h*30*7.5, 2)} for a, h in usage_data.items()]
                df = pd.DataFrame(breakdown)
                total = df["Cost (INR)"].sum()
                st.table(df)
                st.subheader(f"Total Monthly Estimate: INR {total:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'compare':
    if st.button("⬅ MENU"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.header("Appliance-Wise Monthly Comparison")
    selected_compare = st.multiselect("Select Appliances to Compare:", list(app_lib.keys()))
    
    if selected_compare:
        comparison_data = []
        for app in selected_compare:
            st.markdown(f"**Usage for {app}**")
            c1, c2 = st.columns(2)
            with c1:
                h_prev = st.number_input(f"Last Month Hrs", 0.0, 24.0, 1.0, key=f"p_{app}")
            with c2:
                h_curr = st.number_input(f"This Month Hrs", 0.0, 24.0, 1.0, key=f"cu_{app}")
            
            comparison_data.append({
                "Appliance": app,
                "Last Month (INR)": round(app_lib[app]*h_prev*30*7.5, 2),
                "Current Month (INR)": round(app_lib[app]*h_curr*30*7.5, 2),
                "Diff": round((app_lib[app]*h_curr*30*7.5) - (app_lib[app]*h_prev*30*7.5), 2)
            })

        if st.button("RUN DEEP ANALYSIS"):
            df_comp = pd.DataFrame(comparison_data)
            st.bar_chart(df_comp.set_index("Appliance")[["Last Month (INR)", "Current Month (INR)"]])
            
            total_diff = df_comp["Current Month (INR)"].sum() - df_comp["Last Month (INR)"].sum()
            
            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.title("🤖 AI Auditor Report")
            if total_diff > 0:
                culprit = df_comp.loc[df_comp['Diff'].idxmax()]['Appliance']
                st.error(f"Bill Increased by INR {total_diff:,.2f}.")
                st.write(f"Major Factor: Increase in **{culprit}** usage. Try reducing its hours to save money.")
            elif total_diff < 0:
                st.success(f"Bill Decreased by INR {abs(total_diff):,.2f}! Excellent progress.")
            else:
                st.info("No change in consumption detected.")
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
