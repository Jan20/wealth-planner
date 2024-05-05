from abc import abstractmethod, ABC

from pandas import DataFrame

from app.domain.entities.loan_request import LoanRequest
from app.domain.entities.portfolio_request import PortfolioRequest


class LoanForecastUseCase(ABC):

    @staticmethod
    @abstractmethod
    def create_forecast(loan_request: LoanRequest) -> DataFrame:
        """
        Abstract method to create a schedule based on the given portfolio request.

        Parameters:
        - portfolio_request (PortfolioRequest): Object representing the portfolio request.

        Returns:
        - DataFrame: DataFrame representing the schedule created based on the portfolio request.
        """
        pass
