import pandas as pd


class LoanCalculator:
    def __init__(self, loan_amount, tenure, interest, prepayments=None):
        self.loan_amount = loan_amount
        self.tenure = tenure
        self.interest = interest
        self.R = interest / (12 * 100)  # Monthly interest rate
        self.N = tenure * 12            # Total number of months
        self.prepayments = prepayments if prepayments else {}

    def emi(self):
        """Calculate the fixed monthly EMI."""
        return (
            self.loan_amount
            * self.R
            * (1 + self.R) ** self.N
            / ((1 + self.R) ** self.N - 1)
        )

    def generate_schedule(self):
        """Generate the loan amortization schedule."""

        loan_report = []
        outstanding_principal = self.loan_amount
        calculated_emi = round(self.emi(), 2)

        for month in range(1, self.N + 1):

            interest_paid = round(outstanding_principal * self.R, 2)
            principal_paid = round(calculated_emi - interest_paid, 2)

            extra_payment = self.prepayments.get(month, 0)

            outstanding_principal = round(
                outstanding_principal - principal_paid - extra_payment,
                2,
            )

            if outstanding_principal < 0:
                outstanding_principal = 0

            loan_report.append(
                {
                    "Month": month,
                    "EMI": calculated_emi,
                    "Interest Paid": interest_paid,
                    "Principal Paid": principal_paid,
                    "Prepayment": extra_payment,
                    "Outstanding Loan": outstanding_principal,
                }
            )

            if outstanding_principal == 0:
                break

        return pd.DataFrame(loan_report)
    

