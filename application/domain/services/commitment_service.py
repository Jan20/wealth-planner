from application.domain.entities.yearly_commitment import Commitment
from application.use_cases.commitment_usecase import CommitmentUseCase


class CommitmentService(CommitmentUseCase):
    MONTHLY_CONTRIBUTION: float = 150.0
    YEARLY_INTEREST_RATE: float = 0.03
    NUM_YEARS: int = 35
    ANNUAL_GROWTH_RATE: float = 1.06
    FEE_RATE: float = 0.0097
    TAX_DEDUCTIBLE_RATE: float = 0.20
    BASE_YEAR: int = 2024
    SUM_YEAR: int = 2060

    @staticmethod
    def compute_commitment() -> list[Commitment]:
        """
        Computes financial commitments over a specified number of years.

        Returns:
            list[Commitment]: List of Commitment objects representing yearly financial commitments.
        """
        # Initialize commitments list
        commitments: list[Commitment] = []

        # Initial values
        current_year: int = CommitmentService.BASE_YEAR
        contribution: float = CommitmentService.MONTHLY_CONTRIBUTION * 12

        # Compute commitments for each year
        for _ in range(CommitmentService.NUM_YEARS):
            # Calculate fees
            fees: float = CommitmentService.compute_fees(commitments[-1].portfolio, contribution) if commitments else 0

            # Calculate portfolio
            portfolio: float = CommitmentService.compute_portfolio(commitments[-1].portfolio,
                                                                   contribution) if commitments else contribution

            # Calculate tax deductible
            tax_deductible: float = CommitmentService.compute_tax_deductible_amount(contribution)

            # Create yearly commitment
            yearly_commitment = Commitment(
                year=current_year,
                contribution=round(contribution, 2),
                fees=fees,
                portfolio=portfolio,
                tax_deductible=tax_deductible
            )

            # Add yearly commitment to listr
            commitments.append(yearly_commitment)

            # Update contribution and year for next iteration
            contribution *= (1 + CommitmentService.YEARLY_INTEREST_RATE)
            current_year += 1

        # Compute sum of commitments
        return CommitmentService.compute_sum(commitments)

    @staticmethod
    def compute_portfolio(previous_portfolio: float, contribution: float) -> float:
        """
        Computes the portfolio value for the next period.

        Args:
            previous_portfolio (float): The value of the portfolio in the previous period.
            contribution (float): The contribution amount for the current period.

        Returns:
            float: The computed portfolio value for the next period.
        """
        return round(previous_portfolio * CommitmentService.ANNUAL_GROWTH_RATE + contribution, 2)

    @staticmethod
    def compute_tax_deductible_amount(contribution: float) -> float:
        """
          Computes the tax-deductible amount based on the contribution.

          Args:
              contribution (float): The contribution amount for which tax-deductible is calculated.

          Returns:
              float: The computed tax-deductible amount.
          """
        return round(contribution * CommitmentService.TAX_DEDUCTIBLE_RATE, 2)

    @staticmethod
    def compute_fees(previous_portfolio: float, contribution: float) -> float:
        """
        Computes the fees based on the expected development of the portfolio.

        Args:
            previous_portfolio (float): The value of the portfolio in the previous period.
            contribution (float): The contribution amount for the current period.

        Returns:
            float: The computed fees.
        """
        expected_development = previous_portfolio * CommitmentService.ANNUAL_GROWTH_RATE + contribution
        after_fee_development = previous_portfolio * (CommitmentService.ANNUAL_GROWTH_RATE - CommitmentService.FEE_RATE) + contribution
        return round(expected_development - after_fee_development, 2)

    @staticmethod
    def compute_sum(commitments: list[Commitment]) -> list[Commitment]:
        """
        Computes the sum of contributions, tax deductibles, and fees for a list of commitments.

        Args:
            commitments (list[Commitment]): A list of Commitment objects.

        Returns:
            list[Commitment]: The list of Commitment objects with an additional yearly commitment for the sum.
        """
        sum_contributions = sum(commitment.contribution for commitment in commitments)
        sum_deductible = sum(commitment.tax_deductible for commitment in commitments)
        sum_fees = sum(commitment.fees for commitment in commitments)

        yearly_commitment = Commitment(
            year=CommitmentService.SUM_YEAR,
            contribution=sum_contributions,
            fees=sum_fees,
            portfolio=commitments[-1].portfolio,
            tax_deductible=round(sum_deductible, 2)
        )
        commitments.append(yearly_commitment)

        return commitments
