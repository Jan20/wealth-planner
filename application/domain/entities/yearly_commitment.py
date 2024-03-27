from dataclasses import dataclass


@dataclass
class Commitment:
    year: int
    contribution: float
    fees: float
    portfolio: float
    tax_deductible: float
    
    def __str__(self):
        return f"year: {self.year}, Contribution: {self.contribution}"

    def __repr__(self):
        return str(self)
