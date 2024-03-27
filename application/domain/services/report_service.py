from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, TableStyle

from application.domain.entities.yearly_commitment import Commitment
from application.domain.services.commitment_service import CommitmentService
from application.use_cases.report_usecase import ReportUseCase


class ReportService(ReportUseCase):

    def __init__(self, commitmentService: CommitmentService):
        self.commitmentService: CommitmentService = commitmentService

    def generate_report(self):
        """Generates a financial report."""

        canvas = Canvas("report.pdf", pagesize=letter)

        try:
            # Set the font and draw the report title
            canvas.setFont(psfontname="Helvetica", size=24)
            canvas.drawString(x=75, y=720, text="Financial Commitment")

            # Create and draw the table
            table = self.create_table()
            table.wrapOn(canvas, aW=0, aH=0)
            table.drawOn(canvas, x=75, y=20)

        finally:
            canvas.save()

    def create_table(self) -> Table:
        # Get commitments directly from the service
        commitments: list[Commitment] = self.commitmentService.compute_commitment()

        # Define column headers
        column_headers = ["Year", "Contribution", "Fees", "Portfolio", "Deductible"]

        # Extract data for the table
        data = [column_headers] + [[
            commitment.year,
            commitment.contribution,
            commitment.fees,
            commitment.portfolio,
            commitment.tax_deductible
        ] for commitment in commitments]

        # Compute column widths
        width, _ = A4
        col_widths = [width / len(data[0]) - 32] * len(data[0])

        # Create table and apply style
        table = Table(data=data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
         ]))

        # Set fixed height for table rows
        table.height = 10

        return table
