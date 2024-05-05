from app.domain.entities.pension_contribution import PensionContribution
from app.domain.entities.pension_request import PensionRequest
from app.use_cases.pension.pension_use_case import PensionUseCase


class PensionService(PensionUseCase):
    @staticmethod
    def create_pension(pension_request: PensionRequest) -> list[PensionContribution]:
        """
        Computes financial commitments over a specified number of years.

        Returns:
            list[PensionContribution]: List of Commitment objects representing yearly financial commitments.
        """
        NUM_YEARS = pension_request.num_years
        ANNUAL_GROWTH_RATE = pension_request.annual_growth_rate
        FEE_RATE = pension_request.fee_rate
        TAX_DEDUCTIBLE_RATE = pension_request.tax_deductible_rate

        commitments: list[PensionContribution] = []

        # Initial values
        current_year: int = pension_request.base_year
        contribution: float = pension_request.monthly_contribution * 12

        # Compute commitments for each year
        for _ in range(pension_request.sum_year):
            # Calculate fees
            fees: float = PensionService.compute_fees(commitments[-1].portfolio, contribution) if commitments else 0

            # Calculate portfolio
            portfolio: float = PensionService.compute_portfolio(commitments[-1].portfolio,
                                                                contribution) if commitments else contribution

            # Calculate tax deductible
            tax_deductible: float = PensionService.compute_tax_deductible_amount(contribution)

            # Create yearly commitment
            yearly_commitment = PensionContribution(
                year=current_year,
                contribution=round(contribution, 2),
                fees=fees,
                portfolio=portfolio,
                tax_deductible=tax_deductible
            )

            # Add yearly commitment to listr
            commitments.append(yearly_commitment)

            # Update contribution and year for next iteration
            contribution *= (1 + pension_request.yearly_interest_rate)
            current_year += 1

        # Compute sum of commitments
        return PensionService.compute_sum(commitments)

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
        return round(previous_portfolio * PensionService.ANNUAL_GROWTH_RATE + contribution, 2)

    @staticmethod
    def compute_tax_deductible_amount(contribution: float) -> float:
        """
          Computes the tax-deductible amount based on the contribution.

          Args:
              contribution (float): The contribution amount for which tax-deductible is calculated.

          Returns:
              float: The computed tax-deductible amount.
          """
        return round(contribution * PensionService.TAX_DEDUCTIBLE_RATE, 2)

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
        expected_development = previous_portfolio * PensionService.ANNUAL_GROWTH_RATE + contribution
        after_fee_development = previous_portfolio * (PensionService.ANNUAL_GROWTH_RATE - PensionService.FEE_RATE) + contribution
        return round(expected_development - after_fee_development, 2)

    @staticmethod
    def compute_sum(commitments: list[PensionContribution]) -> list[PensionContribution]:
        """
        Computes the sum of contributions, tax deductibles, and fees for a list of commitments.

        Args:
            commitments (list[PensionContribution]): A list of Commitment objects.

        Returns:
            list[Commitment]: The list of Commitment objects with an additional yearly commitment for the sum.
        """
        sum_contributions = sum(commitment.contribution for commitment in commitments)
        sum_deductible = sum(commitment.tax_deductible for commitment in commitments)
        sum_fees = sum(commitment.fees for commitment in commitments)

        yearly_commitment = PensionContribution(
            year=PensionService.SUM_YEAR,
            contribution=sum_contributions,
            fees=sum_fees,
            portfolio=commitments[-1].portfolio,
            tax_deductible=round(sum_deductible, 2)
        )
        commitments.append(yearly_commitment)

        return commitments
