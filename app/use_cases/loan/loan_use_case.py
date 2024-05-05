from abc import abstractmethod, ABC

import pandas as pd

from app.domain.entities.loan_request import LoanRequest


class LoanUseCase(ABC):

    @staticmethod
    @abstractmethod
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
