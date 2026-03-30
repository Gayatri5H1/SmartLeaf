from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
import os


def generate_report(result, output_path):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 🔥 IMPORTANT: set margins properly
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Title style
    title_style = ParagraphStyle(
        name="TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        spaceAfter=20
    )

    # Heading style
    heading_style = ParagraphStyle(
        name="HeadingStyle",
        parent=styles["Heading2"],
        spaceAfter=10
    )

    # 🔥 IMPORTANT: force wrapping width
    normal_style = ParagraphStyle(
        name="NormalStyle",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,   # line spacing
        wordWrap='LTR'
    )

    content = []

    # ---------------- TITLE ----------------
    content.append(Paragraph("SMARTLEAF CROP HEALTH REPORT", title_style))
    content.append(Spacer(1, 15))

    # ---------------- BASIC INFO ----------------
    content.append(Paragraph(f"<b>Crop:</b> {result['crop']}", normal_style))
    content.append(Paragraph(f"<b>Disease:</b> {result['disease']}", normal_style))
    content.append(Paragraph(f"<b>Confidence:</b> {result['confidence']}%", normal_style))
    content.append(Paragraph(f"<b>Severity:</b> {result['severity']}", normal_style))

    content.append(Spacer(1, 20))

    # ---------------- TREATMENT ----------------
    content.append(Paragraph("Recommended Treatment", heading_style))
    content.append(Spacer(1, 10))

    # 🔥 KEY FIX: wrap long text properly
    content.append(Paragraph(f"<b>Chemical:</b> {result['chemical']}", normal_style))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Organic:</b> {result['organic']}", normal_style))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Prevention:</b> {result['prevention']}", normal_style))

    # ---------------- BUILD ----------------
    doc.build(content)