from dataclasses import dataclass

from pandas import Timestamp


@dataclass
class LoanRequest:
    principal: float
    annual_interest_rate: float
    start_date: Timestamp
    end_date: Timestamp
