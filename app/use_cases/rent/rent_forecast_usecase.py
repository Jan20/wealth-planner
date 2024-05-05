from abc import ABC, abstractmethod

from app.domain.entities.rent_request import RentRequest


class RentForecastUseCase(ABC):

    @abstractmethod
    def create_forecast(self, rent_request: RentRequest):
        pass
