from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(notes, filename="study_notes.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = [
        Paragraph("AI Study Notes", styles["Title"]),
        Paragraph(notes.replace("\n", "<br/>"), styles["BodyText"])
    ]

    doc.build(content)

    return filename