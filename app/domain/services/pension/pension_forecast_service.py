import io
import locale
import os
from os.path import exists

from matplotlib.figure import Figure
from pandas import DataFrame
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.platypus import Table

from app.domain.entities.pension_request import PensionRequest
from app.use_cases.pension.pension_forecast_use_case import PensionForecastUseCase
from app.use_cases.pension.pension_use_case import PensionUseCase


class PensionForecastService(PensionForecastUseCase):
    def __init__(self, pension_use_case: PensionUseCase):
        self.pension_use_case: PensionUseCase = pension_use_case

    def create_forecast(self, pension_request: PensionRequest):
        self.delete_document(file_path="files/forecast.pdf")

        df = self.pension_use_case.create_pension(pension_request)

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

        # Plot DataFrame using Matplotlib
        ax = figure.subplots()

        ax.plot(df['Year'], df['Portfolio'], marker='o', color='green', label='Portfolio')
        ax.fill_between(df['Year'], df['Portfolio'], color='green', alpha=0.3)
        ax.set_xlabel('Year')
        ax.set_ylabel('Portfolio')
        ax.legend()

        # Save it to a temporary buffer.
        buffer = io.BytesIO()
        figure.savefig(buffer, format="png", dpi=600)
        return Image(buffer, width=440, height=300)

    @staticmethod
    def generate_table(df: DataFrame) -> Table:
        updated_df = df.copy()

        updated_df["Portfolio"] = updated_df["Portfolio"].map(
            lambda x: locale.currency(x, symbol=True, grouping=True, international=True))

        # Convert DataFrame to list of lists for table data
        data = [updated_df.columns.tolist()] + updated_df.values.tolist()

        # Create Table object
        return Table(data, colWidths=113, style=[
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOTTOMMARGIN', (0, 0), (-1, -1), 10, colors.black)
        ])

    @staticmethod
    def delete_document(file_path: str):
        # Check if the file exists before attempting to delete it
        if exists(file_path):
            os.remove(file_path)
