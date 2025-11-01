from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def generate_pdf_from_text(title: str, content: str) -> BytesIO:
    """
    Simple PDF generator using ReportLab. Returns a BytesIO buffer ready to be saved.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    c.setFillColor(colors.HexColor("#222222"))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, height - 2 * cm, title[:100] if title else "Note")

    # Body text (simple wrapping)
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11)
    left_margin = 2 * cm
    top = height - 3 * cm
    max_width = width - 4 * cm

    def wrap_text(text: str, line_width: float):
        words = (text or "").split()
        lines = []
        line = ""
        for w in words:
            test = (line + " " + w).strip()
            if c.stringWidth(test, "Helvetica", 11) <= line_width:
                line = test
            else:
                lines.append(line)
                line = w
        if line:
            lines.append(line)
        return lines

    y = top
    for paragraph in (content or "").split("\n\n"):
        lines = wrap_text(paragraph, max_width)
        for ln in lines:
            if y < 2 * cm:
                c.showPage()
                y = height - 2 * cm
                c.setFont("Helvetica", 11)
            c.drawString(left_margin, y, ln)
            y -= 14
        y -= 10

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


