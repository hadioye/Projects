from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(business_details, competitors):
    c = canvas.Canvas("business_analysis.pdf", pagesize=letter)
    width, height = letter

    # Business details
    c.drawString(100, height - 100, f"Business Name: {business_details['name']}")
    c.drawString(100, height - 120, f"Address: {business_details['address']}")
    c.drawString(100, height - 140, f"Phone: {business_details['phone']}")
    c.drawString(100, height - 160, f"Hours: {business_details['hours']}")

    # Insert business rating screenshot
    c.drawImage('rating.png', 100, height - 300, width=200, height=100)

    # Competitor details
    y_position = height - 400
    for i, competitor in enumerate(competitors):
        c.drawString(100, y_position, f"Competitor {i+1} Name: {competitor['name']}")
        c.drawString(100, y_position - 20, f"Rating: {competitor['rating']}")
        c.drawImage(f'competitor_{i}.png', 100, y_position - 140, width=200, height=100)
        y_position -= 200

    c.save()
