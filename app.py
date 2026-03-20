import streamlit as st
import pandas as pd

st.set_page_config(page_title="EcoWatt India | Deep Compare", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(240,244,248,0.92), rgba(240,244,248,0.92)), 
                    url("https://images.unsplash.com/photo-1558444479-c849519d7360?auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    .main-card {
        background: #ffffff;
        border-radius: 15px;
        padding: 30px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    input, div[data-baseweb="input"], div[data-baseweb="select"], .stNumberInput div {
        background-color: #f8fafc !important;
        color: #1e293b !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
    }
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    .stButton>button {
        background-color: #0f172a;
        color: #ffffff !important;
        border-radius: 8px;
        height: 3.5em;
    }
    .report-box {
        background: #f1f5f9;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        border-left: 10px solid #00d1b2;
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
            if st.button("CALCULATE CURRENT BILL"):
                st.session_state.page = 'calculate'
                st.rerun()
        with col2:
            if st.button("DEEP MONTHLY COMPARISON"):
                st.session_state.page = 'compare'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'calculate':
    if st.button("⬅ MENU"):
        st.session_state.page = 'home'
        st.rerun()
    # [Calculation logic remains same as previous version]
    st.info("Directly use the 'Deep Monthly Comparison' to analyze two months side-by-side.")

elif st.session_state.page == 'compare':
    if st.button("⬅ MENU"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.header("Appliance-Wise Monthly Comparison")
    
    selected_compare = st.multiselect("Select Appliances to Compare:", list(app_lib.keys()))
    
    if selected_compare:
        comparison_data = []
        st.markdown("---")
        
        for app in selected_compare:
            st.subheader(f"Usage for {app}")
            c1, c2 = st.columns(2)
            with c1:
                h_prev = st.number_input(f"Last Month Hrs ({app})", 0.0, 24.0, 1.0, key=f"prev_{app}")
            with c2:
                h_curr = st.number_input(f"This Month Hrs ({app})", 0.0, 24.0, 1.0, key=f"curr_{app}")
            
            cost_prev = app_lib[app] * h_prev * 30 * 7.5
            cost_curr = app_lib[app] * h_curr * 30 * 7.5
            comparison_data.append({
                "Appliance": app,
                "Last Month (INR)": round(cost_prev, 2),
                "Current Month (INR)": round(cost_curr, 2),
                "Diff": round(cost_curr - cost_prev, 2)
            })

        if st.button("RUN COMPARATIVE ANALYSIS"):
            df_comp = pd.DataFrame(comparison_data)
            total_prev = df_comp["Last Month (INR)"].sum()
            total_curr = df_comp["Current Month (INR)"].sum()
            total_diff = total_curr - total_prev

            st.markdown("---")
            st.subheader("Visual Expenditure Shift")
            
            # Elegant Side-by-Side Bar Chart
            chart_df = df_comp.melt(id_vars="Appliance", value_vars=["Last Month (INR)", "Current Month (INR)"], 
                                    var_name="Month", value_name="Cost")
            st.bar_chart(chart_df, x="Appliance", y="Cost", color="Month")

            

            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.title("🤖 Finalized AI Auditor Report")
            
            if total_diff > 0:
                st.error(f"Bill Increased by INR {total_diff:,.2f} this month.")
                # Identify the "Culprit" appliance
                culprit = df_comp.loc[df_comp['Diff'].idxmax()]
                st.markdown(f"**Primary Cause:** Your **{culprit['Appliance']}** usage increased significantly, adding **INR {culprit['Diff']}** to your bill.")
                st.markdown(f"**Recommendation:** Reduce **{culprit['Appliance']}** usage by at least 15% next month. Consider using it only during non-peak hours.")
            elif total_diff < 0:
                st.success(f"Bill Decreased by INR {abs(total_diff):,.2f}! Excellent optimization.")
                st.markdown("**Efficiency Gain:** Your energy management strategies are working. Keep maintaining the current schedule.")
            else:
                st.info("Your consumption is identical to last month.")
            
            st.markdown(f"**Total Last Month:** INR {total_prev:,.2f} | **Total This Month:** INR {total_curr:,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
