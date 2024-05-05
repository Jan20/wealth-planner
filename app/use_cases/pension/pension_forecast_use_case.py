from abc import abstractmethod, ABC

from pandas import DataFrame

from app.domain.entities.pension_request import PensionRequest


class PensionForecastUseCase(ABC):

    @staticmethod
    @abstractmethod
    def create_forecast(pension_request: PensionRequest) -> DataFrame:
        """
        Abstract method to create a schedule based on the given portfolio request.

        Parameters:
        - portfolio_request (PortfolioRequest): Object representing the portfolio request.

        Returns:
        - DataFrame: DataFrame representing the schedule created based on the portfolio request.
        """
        pass
