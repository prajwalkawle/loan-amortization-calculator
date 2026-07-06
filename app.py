import io
import pandas as pd
import streamlit as st
from main import LoanCalculator

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Smart Loan Amortization Engine",
    layout="wide"
)

st.title("📊 Smart Loan Amortization Engine")
st.markdown(
    "Calculate EMI, visualize your amortization schedule, and analyze the impact of prepayments."
)

# ---------------------------------------------------
# Sidebar Inputs
# ---------------------------------------------------
st.sidebar.header("🕹️ Loan Parameters")

loan_amount = st.sidebar.number_input(
    "Loan Amount (INR)",
    min_value=1000,
    max_value=10000000,
    value=500000,
    step=10000,
)

tenure = st.sidebar.slider(
    "Loan Tenure (Years)",
    min_value=1,
    max_value=30,
    value=5,
)

interest = st.sidebar.slider(
    "Annual Interest Rate (%)",
    min_value=1.0,
    max_value=25.0,
    value=12.0,
    step=0.1,
)

# ---------------------------------------------------
# Prepayment Inputs
# ---------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.header("💰 Prepayment")

prepay_month = st.sidebar.number_input(
    "Prepayment Month",
    min_value=1,
    max_value=tenure * 12,
    value=12,
)

prepay_amount = st.sidebar.number_input(
    "Prepayment Amount (INR)",
    min_value=0,
    max_value=int(loan_amount),
    value=50000,
    step=5000,
)

prepayments_dict = {}

if prepay_amount > 0:
    prepayments_dict[prepay_month] = prepay_amount

# ---------------------------------------------------
# Loan Calculation
# ---------------------------------------------------
calculator = LoanCalculator(
    loan_amount,
    tenure,
    interest,
    prepayments=prepayments_dict,
)

df_schedule = calculator.generate_schedule()

# ---------------------------------------------------
# Executive Summary
# ---------------------------------------------------
st.subheader("🏁 Executive Summary")

col1, col2, col3 = st.columns(3)

total_interest = df_schedule["Interest Paid"].sum()
total_prepayment = df_schedule["Prepayment"].sum()
total_outflow = df_schedule["EMI"].sum() + total_prepayment
months_to_pay = len(df_schedule)

with col1:
    st.metric(
        "Loan Closed In",
        f"{months_to_pay} Months"
    )

with col2:
    st.metric(
        "Total Interest Paid",
        f"₹{total_interest:,.2f}"
    )

with col3:
    st.metric(
        "Total Cash Outflow",
        f"₹{total_outflow:,.2f}"
    )

st.divider()

# ---------------------------------------------------
# Balance Chart
# ---------------------------------------------------
st.subheader("📉 Outstanding Loan Balance")

st.line_chart(
    df_schedule.set_index("Month")["Outstanding Loan"]
)

# ---------------------------------------------------
# Amortization Table
# ---------------------------------------------------
st.subheader("📋 Amortization Schedule")

st.dataframe(
    df_schedule,
    use_container_width=True,
)

# ---------------------------------------------------
# Download Excel Report
# ---------------------------------------------------
buffer = io.BytesIO()

with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df_schedule.to_excel(writer, index=False)

st.download_button(
    label="📥 Download Excel Report",
    data=buffer.getvalue(),
    file_name="Loan_Amortization_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)