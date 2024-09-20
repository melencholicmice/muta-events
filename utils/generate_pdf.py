import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings
from io import BytesIO

def generate_pdf( 
        payment_id, 
        user_first_name, 
        user_last_name, 
        payment_amount, 
        payment_boolean, 
        stripe_checkout_session_id,
        created_at
    ):
    static_dir = os.path.join(settings.BASE_DIR, 'static')
    # Ensure static folder exists
    os.makedirs(static_dir, exist_ok=True)

    # Full path for saving the PDF
    filename = f'payment_{payment_id}.pdf'
    file_path = os.path.join(static_dir, filename)

    # Create a BytesIO buffer to hold the PDF content
    buffer = BytesIO()

    # Create a PDF document using SimpleDocTemplate with the buffer
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []

    styles = getSampleStyleSheet()

    title = "Payment Invoice"

    elements.append(Paragraph(title, styles['Title']))

    invoice_info = [
        ['Payment ID:', str(payment_id)],
        ['User:', f'{user_first_name} {user_last_name}'],
        ['Payment Amount:', f'{payment_amount}'],
        ['Payment Status:', 'Successful' if payment_boolean else 'Failed'],
        ['Checkout Session ID:', stripe_checkout_session_id],
        ['Created At:', created_at],
    ]

    table = Table(invoice_info, colWidths=[150, 400])

    # Style the table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    footer_text = "Thank you for your payment! We appreciate your business. Please keep this invoice for your records. If you have any questions or concerns, please don't hesitate to contact our customer support team. For future reference, you can find our terms of service and refund policy on our website."
    footer = Paragraph(footer_text, styles['Normal'])
    elements.append(footer)

    # Build the PDF content
    pdf.build(elements)

    # Get the value of the BytesIO buffer and write it to the file
    pdf_content = buffer.getvalue()
    with open(file_path, 'wb') as f:
        f.write(pdf_content)

    return file_path