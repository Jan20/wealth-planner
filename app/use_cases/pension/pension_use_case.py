from abc import abstractmethod, ABC

from app.domain.entities.pension_contribution import PensionContribution
from app.domain.entities.pension_request import PensionRequest


class PensionUseCase(ABC):

    @staticmethod
    @abstractmethod
    def create_pension(pension_request: PensionRequest) -> list[PensionContribution]:
        """
        Computes financial commitments over a specified number of years.

        Returns:
            list[PensionContribution]: List of Commitment objects representing yearly financial commitments.
        """
        pass
