import pandas as pd
import matplotlib.pyplot as plt 

def calculate(principal: float, term: int, rate: float):
    mr = rate/12. 
    adj_term = convert_year_to_month(term[0])+term[1]
    p = (1+mr)**(adj_term)
    monthly_payment = principal*((mr*p)/(p-1))
    monthly_interest = principal*(mr)
    total_interest = monthly_payment*adj_term - principal 
    total_amount = total_interest + monthly_payment*adj_term 
    return monthly_payment, monthly_interest, total_interest, total_amount 

def convert_year_to_month(years):
    return years*12 

def amortization_schedule(principal: float, annual_rate: float, years: int) -> pd.DataFrame:
    """
    Build an amortization table for a fixed-rate loan.

    Args:
        principal: Original loan amount
        annual_rate: Annual interest rate as a percent (example: 6.5 for 6.5%)
        years: Loan term in years

    Returns:
        pandas DataFrame with the amortization schedule
    """
    monthly_rate = annual_rate / 100 / 12
    total_payments = years * 12

    # Monthly payment formula
    monthly_payment = principal * (
        monthly_rate * (1 + monthly_rate) ** total_payments
    ) / ((1 + monthly_rate) ** total_payments - 1)

    balance = principal
    schedule = []

    for payment_number in range(1, total_payments + 1):
        interest_payment = balance * monthly_rate
        principal_payment = monthly_payment - interest_payment

        # Prevent tiny floating-point overrun on final payment
        if principal_payment > balance:
            principal_payment = balance
            monthly_payment = principal_payment + interest_payment

        ending_balance = balance - principal_payment

        schedule.append({
            "Payment #": payment_number,
            "Beginning Balance": round(balance, 2),
            "Monthly Payment": round(monthly_payment, 2),
            "Principal Paid": round(principal_payment, 2),
            "Interest Paid": round(interest_payment, 2),
            "Ending Balance": round(ending_balance, 2),
        })

        balance = ending_balance

        if balance <= 0:
            break
            
    df = pd.DataFrame(schedule)
    return df

    plt.tight_layout()
    plt.show()

    return df

