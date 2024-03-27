from abc import abstractmethod, ABC

from application.domain.entities.yearly_commitment import Commitment


class CommitmentUseCase(ABC):

    @staticmethod
    @abstractmethod
    def compute_commitment() -> list[Commitment]:
        """
        Computes financial commitments over a specified number of years.

        Returns:
            list[Commitment]: List of Commitment objects representing yearly financial commitments.
        """
        pass
