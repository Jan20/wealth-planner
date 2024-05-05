from dataclasses import dataclass

from pandas import Timestamp


@dataclass
class RentRequest:
    monthly_rent: float
    annual_increase: float
    start_date: Timestamp
    end_date: Timestamp
