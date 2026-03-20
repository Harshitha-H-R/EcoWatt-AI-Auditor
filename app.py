import streamlit as st
import pandas as pd

st.set_page_config(page_title="EcoWatt India", layout="wide")

# Clean CSS
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
}
h1, h2, h3, h4, h5, h6, p, label {
    color: #000000;
}
.main-card {
    background: #ffffff;
    padding: 25px;
    border-radius: 10px;
    border: 1px solid #ccc;
}
.stButton>button {
    background-color: #000000;
    color: #ffffff;
    height: 2.8em;
}
</style>
""", unsafe_allow_html=True)

# Navigation state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Appliance power (kW)
app_lib = {
    "Refrigerator": 0.25, "Washing Machine": 0.5, "Dishwasher": 1.5,
    "Air Conditioner": 1.5, "Electric Oven": 2.0, "Microwave Oven": 1.0,
    "Vacuum Cleaner": 0.8, "Electric Iron": 1.1, "Television": 0.1,
    "Computer": 0.2, "Hair Dryer": 1.5, "Electric Fan": 0.07,
    "Electric Kettle": 1.5, "Toaster": 0.8
}

RATE = 7.5  # INR per kWh

# ---------------- HOME ----------------
if st.session_state.page == 'home':
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("EcoWatt India")
    st.subheader("Energy Consumption Analysis System")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Calculate Bill"):
            st.session_state.page = 'calculate'
            st.rerun()

    with col2:
        if st.button("Compare Monthly Usage"):
            st.session_state.page = 'compare'
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- CALCULATE ----------------
elif st.session_state.page == 'calculate':
    if st.button("Back"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.header("Appliance Energy Audit")

    name = st.text_input("Customer Name")

    if name:
        selected = st.multiselect("Select Appliances", list(app_lib.keys()))

        if selected:
            usage_data = {}
            st.subheader("Enter Daily Usage (Hours)")

            cols = st.columns(3)

            for i, app in enumerate(selected):
                with cols[i % 3]:
                    usage_data[app] = st.number_input(
                        f"{app}", 0.0, 24.0, 1.0, key=app
                    )

            if st.button("Generate Report"):
                data = []
                total_energy = 0

                for app, hrs in usage_data.items():
                    energy = app_lib[app] * hrs * 30  # kWh/month
                    cost = energy * RATE
                    total_energy += energy

                    data.append({
                        "Appliance": app,
                        "Power (kW)": app_lib[app],
                        "Monthly Energy (kWh)": round(energy, 2),
                        "Cost (INR)": round(cost, 2)
                    })

                df = pd.DataFrame(data)

                st.table(df)

                total_cost = df["Cost (INR)"].sum()

                st.subheader(f"Total Energy: {total_energy:.2f} kWh")
                st.subheader(f"Estimated Bill: INR {total_cost:,.2f}")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- COMPARE ----------------
elif st.session_state.page == 'compare':
    if st.button("Back"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.header("Monthly Comparison")

    selected_compare = st.multiselect("Select Appliances", list(app_lib.keys()))

    if selected_compare:
        comparison_data = []

        for app in selected_compare:
            st.write(f"{app}")

            col1, col2 = st.columns(2)

            with col1:
                prev = st.number_input(f"Last Month (hrs/day)", 0.0, 24.0, 1.0, key=f"p_{app}")
            with col2:
                curr = st.number_input(f"Current Month (hrs/day)", 0.0, 24.0, 1.0, key=f"c_{app}")

            prev_cost = app_lib[app] * prev * 30 * RATE
            curr_cost = app_lib[app] * curr * 30 * RATE

            comparison_data.append({
                "Appliance": app,
                "Last Month (INR)": round(prev_cost, 2),
                "Current Month (INR)": round(curr_cost, 2)
            })

        if st.button("Analyze"):
            df = pd.DataFrame(comparison_data)

            st.bar_chart(df.set_index("Appliance"))

            total_prev = df["Last Month (INR)"].sum()
            total_curr = df["Current Month (INR)"].sum()

            diff = total_curr - total_prev

            st.subheader("Analysis Report")

            if diff > 0:
                st.error(f"Electricity bill increased by INR {diff:,.2f}")
                st.write("Recommendation: Reduce usage of high power appliances.")
            else:
                st.success(f"Electricity bill reduced by INR {abs(diff):,.2f}")
                st.write("Good energy management observed.")

    st.markdown('</div>', unsafe_allow_html=True)
    
