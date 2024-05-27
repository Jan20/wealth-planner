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

from app.domain.entities.loan_request import LoanRequest
from app.use_cases.loan.loan_forecast_use_case import LoanForecastUseCase
from app.use_cases.loan.loan_use_case import LoanUseCase


class LoanForecastService(LoanForecastUseCase):
    def __init__(self, loan_use_cast: LoanUseCase):
        self.loan_use_cast: LoanUseCase = loan_use_cast

    def create_forecast(self, loan_request: LoanRequest):
        self.delete_document(file_path="files/forecast.pdf")

        df = self.loan_use_cast.create_loan(loan_request)

        SimpleDocTemplate("files/forecast.pdf", pagesize=letter).build([
            self.create_headline(),
            self.generate_table(df),
            Spacer(1, 1),
            self.create_image(df)
        ])

    @staticmethod
    def create_headline() -> Paragraph:
        return Paragraph(text="Loan Forecast", style=ParagraphStyle(
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
        ax.plot(df['Month'], df['Principal'], color='green', label='Principal')
        ax.plot(df['Month'], df['Interest'], color='red', label='Interest')
        ax.fill_between(df['Month'], df['Principal'], color='green', alpha=0.3)
        ax.fill_between(df['Month'], df['Interest'], color='red', alpha=0.3)
        ax.set_xlabel('Month')
        ax.set_ylabel('Rent Paid')
        ax.legend()

        # Save it to a temporary buffer.
        buffer = io.BytesIO()
        figure.savefig(buffer, format="png", dpi=600)
        return Image(buffer, width=440, height=300)

    @staticmethod
    def generate_table(df: DataFrame) -> Table:
        # Convert DataFrame to list of lists for table data

        print(df['Interest'].sum())
        print(df['Payment'].sum())
        print(df['Principal'].sum())

        table_df = DataFrame()
        table_df['Month'] = df['Month'].map(lambda date: date.strftime("%m %Y"))
        table_df['Payment'] = df['Payment'].map(lambda x: locale.currency(x, symbol=True,  grouping=True, international=True))
        table_df['Interest'] = df['Interest'].map(lambda x: locale.currency(x, symbol=True,  grouping=True, international=True))
        table_df['Principal'] = df['Principal'].map(lambda x: locale.currency(x, symbol=True,  grouping=True, international=True))
        table_df['Remaining Balance'] = df['Remaining Balance'].map(lambda x: locale.currency(x, symbol=True,  grouping=True, international=True))

        data = [table_df.columns.tolist()] + table_df.values.tolist()

        print(table_df['Interest'].sum())

        return Table(data, colWidths=91, style=[
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
