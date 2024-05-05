import io
import os
from os.path import exists

from matplotlib.figure import Figure
from pandas import DataFrame
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.platypus import Table

from app.domain.entities.rent_request import RentRequest
from app.use_cases.rent.rent_use_case import RentUseCase
from app.use_cases.rent.rent_forecast_usecase import RentForecastUseCase


class RentForecastService(RentForecastUseCase):
    def __init__(self, rentUseCase: RentUseCase):
        self.rentUseCase: RentUseCase = rentUseCase

    def create_forecast(self, rent_request: RentRequest):
        self.delete_document("files/forecast.pdf")

        df = self.rentUseCase.create_rent(rent_request)

        SimpleDocTemplate(filename="files/forecast.pdf", pagesize=letter).build([
            self.create_headline(),
            self.generate_table(df),
            Spacer(1, 1),
            self.create_image(df)
        ])

    @staticmethod
    def create_headline() -> Paragraph:
        return Paragraph(text="Rent Forecast", style=ParagraphStyle(
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
        ax.plot(df['Year'], df['Sum'], marker='o', color='red', label='Rent Paid')
        ax.fill_between(df['Year'], df['Sum'], color='red', alpha=0.3)
        ax.set_xlabel('Year')
        ax.set_ylabel('Rent Paid')
        ax.legend()

        # Save it to a temporary buffer.
        buffer = io.BytesIO()
        figure.savefig(buffer, format="png", dpi=600)
        return Image(buffer, width=440, height=300)

    @staticmethod
    def generate_table(df: DataFrame) -> Table:
        # Convert DataFrame to list of lists for table data
        data = [df.columns.tolist()] + df.values.tolist()

        # Create Table object
        return Table(data, colWidths=150, style=[
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
