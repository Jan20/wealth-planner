from abc import abstractmethod, ABC

from pandas import DataFrame

from app.domain.entities.rent_request import RentRequest


class RentUseCase(ABC):

    @staticmethod
    @abstractmethod
    def create_rent(rent_request: RentRequest) -> DataFrame:
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
