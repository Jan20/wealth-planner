import pandas as pd
from pandas import DatetimeIndex

from app.domain.entities.loan_request import LoanRequest
from app.use_cases.loan.loan_use_case import LoanUseCase


class LoanService(LoanUseCase):

    @staticmethod
    def create_loan(loan_request: LoanRequest) -> pd.DataFrame:
        """
        Generate a pandas DataFrame containing the monthly annuity payments,
        the monthly interest being paid, and the principal monthly repayments
        for an annuity loan.

        Args:
        principal (float): The initial loan amount.
        annual_interest_rate (float): Annual interest rate (as a decimal).
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.

        Returns:
        pandas.DataFrame: DataFrame containing the loan schedule.
        """
        date_range: DatetimeIndex = pd.date_range(
            start=loan_request.start_date,
            end=loan_request.end_date,
            freq='M'
        )

        principal = loan_request.principal
        annual_interest_rate = loan_request.annual_interest_rate

        # Convert annual interest rate to monthly interest rate
        monthly_interest_rate = annual_interest_rate / 12

        # Calculate the monthly payment using the annuity formula
        monthly_payment = principal * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -len(date_range))

        # Initialize lists to store data
        payment_list = []
        interest_list = []
        principal_list = []
        remaining_balance_list = []

        # Initialize remaining balance
        remaining_balance = principal

        # Generate loan schedule
        for i in range(len(date_range)):
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment
            principal_payment = min(principal_payment, remaining_balance)
            remaining_balance -= principal_payment

            payment_list.append(monthly_payment)
            interest_list.append(interest_payment)
            principal_list.append(principal_payment)
            remaining_balance_list.append(remaining_balance)

        loan_schedule_df = pd.DataFrame({
            'Month': date_range,
            'Payment': payment_list,
            'Interest': interest_list,
            'Principal': principal_list,
            'Remaining Balance': remaining_balance_list
        })

        return loan_schedule_df
