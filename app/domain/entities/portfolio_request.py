from dataclasses import dataclass

from pandas import Timestamp


@dataclass
class PortfolioRequest:
    initial_portfolio: float
    yearly_return: float
    yearly_contribution: float
    start_date: Timestamp
    end_date: Timestamp
