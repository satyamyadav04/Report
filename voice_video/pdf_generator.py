from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(report_text, filename="final_report.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    x, y = 40, height - 40
    for line in report_text.split("\n"):
        c.drawString(x, y, line)
        y -= 14
        if y < 40:
            c.showPage()
            y = height - 40

    c.save()
