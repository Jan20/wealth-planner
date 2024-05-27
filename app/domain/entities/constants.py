from reportlab.lib import colors

DEFAULT_STYLE = [
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('BOTTOMMARGIN', (0, 0), (-1, -1), 10, colors.black)
]