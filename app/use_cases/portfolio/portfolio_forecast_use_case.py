from abc import ABC, abstractmethod

from app.domain.entities.portfolio_request import PortfolioRequest


class PortfolioForecastUseCase(ABC):

    @abstractmethod
    def create_forecast(self, portfolio_request: PortfolioRequest):
        pass
