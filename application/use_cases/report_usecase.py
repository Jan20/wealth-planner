from abc import ABC, abstractmethod
from reportlab.platypus import Table


class ReportUseCase(ABC):

    @abstractmethod
    def generate_report(self):
        """Generate a financial report for a given year"""
        pass

    @abstractmethod
    def create_table(self) -> Table:
        """Generate a KPI table for the financial report"""
        pass
