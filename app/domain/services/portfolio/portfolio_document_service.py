import io
import locale
import os
from os.path import exists

from matplotlib.figure import Figure
from pandas import DataFrame, concat
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.platypus import Table

from app.domain.entities.constants import DEFAULT_STYLE
from app.domain.entities.portfolio_request import PortfolioRequest
from app.use_cases.portfolio.portfolio_forecast_use_case import PortfolioForecastUseCase
from app.use_cases.portfolio.portfolio_use_case import PortfolioUseCase


class PortfolioForecastService(PortfolioForecastUseCase):
    def __init__(self, portfolio_use_case: PortfolioUseCase):
        self.portfolio_use_case: PortfolioUseCase = portfolio_use_case

    def create_forecast(self, portfolio_request: PortfolioRequest):
        self.delete_document("files/forecast.pdf")

        df = self.portfolio_use_case.create_portfolio(portfolio_request)

        SimpleDocTemplate(filename="files/forecast.pdf", pagesize=letter).build([
            self.create_headline(),
            self.generate_table(df),
            Spacer(1, 1),
            self.create_image(df)
        ])

    @staticmethod
    def create_headline() -> Paragraph:
        return Paragraph(text="Portfolio Forecast", style=ParagraphStyle(
            name='Headline',
            fontSize=24,
            leading=28,
            spaceAfter=12
        ))

    @staticmethod
    def create_image(df: DataFrame) -> Image:
        figure = Figure()
        ax = figure.subplots()

        ax.plot(df['Year'], df['Portfolio'], marker='o', color='green', label='Portfolio')
        ax.fill_between(df['Year'], df['Portfolio'], color='green', alpha=0.3)
        ax.set_xlabel('Year')
        ax.set_ylabel('Portfolio')
        ax.legend()

        buffer = io.BytesIO()
        figure.savefig(buffer, format="png", dpi=600)
        return Image(buffer, width=440, height=300)

    @staticmethod
    def generate_table(dataframe: DataFrame) -> Table:
        df = concat([dataframe.copy(), DataFrame({
            'Year': 'SUM',
            'Portfolio': dataframe["Portfolio"].iloc[-1] + dataframe["Growth"].iloc[-1] + dataframe["Contribution"].iloc[-1],
            'Growth': dataframe["Growth"].sum(),
            'Contribution': [dataframe["Contribution"].sum()],
        })], ignore_index=True)

        for column in ["Portfolio", "Growth", "Contribution"]:
            df[column] = df[column].map(lambda x: locale.currency(x, symbol=True, grouping=True, international=True))

        return Table([df.columns.tolist()] + df.values.tolist(), colWidths=113, style=DEFAULT_STYLE)

    @staticmethod
    def delete_document(file_path: str):
        if exists(file_path):
            os.remove(file_path)
