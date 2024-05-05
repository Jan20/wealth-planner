from dataclasses import dataclass


@dataclass
class PensionRequest:
    monthly_contribution: float
    yearly_interest_rate: float
    num_years: int
    annual_growth_rate: float
    fee_rate: float
    tax_deductible_rate: float
    base_year: int
    sum_year: int
