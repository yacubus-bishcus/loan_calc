import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from loan_calc import amortization_schedule

def calculate_summary(principal, annual_rate, years):
    df = amortization_schedule(principal, annual_rate, years)
    monthly_payment = df['Monthly Payment'].iloc[0]
    total_interest = df['Interest Paid'].sum()
    total_amount = principal + total_interest
    return monthly_payment, total_interest, total_amount, df

st.title("Loan Comparison App")

st.sidebar.header("Loan 1 Inputs")
principal1 = st.sidebar.number_input("Principal Amount ($)", min_value=0.0, value=100000.0, key="p1")
rate1 = st.sidebar.number_input("Annual Interest Rate (%)", min_value=0.0, value=5.0, key="r1")
term1 = st.sidebar.number_input("Term (years)", min_value=1, value=30, key="t1")

st.sidebar.header("Loan 2 Inputs")
principal2 = st.sidebar.number_input("Principal Amount ($)", min_value=0.0, value=100000.0, key="p2")
rate2 = st.sidebar.number_input("Annual Interest Rate (%)", min_value=0.0, value=6.0, key="r2")
term2 = st.sidebar.number_input("Term (years)", min_value=1, value=30, key="t2")

if st.button("Compare Loans"):
    # Calculate for loan 1
    mp1, ti1, ta1, df1 = calculate_summary(principal1, rate1, term1)
    
    # Calculate for loan 2
    mp2, ti2, ta2, df2 = calculate_summary(principal2, rate2, term2)
    
    # Display comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Loan 1")
        st.write(f"Monthly Payment: ${mp1:.2f}")
        st.write(f"Total Interest: ${ti1:.2f}")
        st.write(f"Total Amount: ${ta1:.2f}")
    
    with col2:
        st.subheader("Loan 2")
        st.write(f"Monthly Payment: ${mp2:.2f}")
        st.write(f"Total Interest: ${ti2:.2f}")
        st.write(f"Total Amount: ${ta2:.2f}")
    
    # Plot overlaid amortization schedules
    st.subheader("Amortization Schedule Comparison")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot cumulative interest
    ax.plot(df1['Payment #'], df1['Interest Paid'].cumsum(), label=f'Loan 1 Cumulative Interest', color='blue')
    ax.plot(df2['Payment #'], df2['Interest Paid'].cumsum(), label=f'Loan 2 Cumulative Interest', color='red')
    
    ax.set_xlabel('Payment Number')
    ax.set_ylabel('Cumulative Interest ($)')
    ax.set_title('Cumulative Interest Over Time')
    ax.legend()
    ax.grid(True)
    
    st.pyplot(fig)
    
    # Also plot ending balance
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(df1['Payment #'], df1['Ending Balance'], label='Loan 1 Ending Balance', color='blue')
    ax2.plot(df2['Payment #'], df2['Ending Balance'], label='Loan 2 Ending Balance', color='red')
    ax2.set_xlabel('Payment Number')
    ax2.set_ylabel('Ending Balance ($)')
    ax2.set_title('Ending Balance Over Time')
    ax2.legend()
    ax2.grid(True)
    
    st.pyplot(fig2)