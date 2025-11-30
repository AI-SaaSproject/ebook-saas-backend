# api/compile_pdf.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER
import requests
from io import BytesIO

router = APIRouter()


class Section(BaseModel):
    section_name: str
    text: str
    image_url: str


class PDFRequest(BaseModel):
    title: str
    author: str
    sections: list[Section]


@router.post("/compile_pdf")
async def compile_pdf(req: PDFRequest):

    try:
        buffer = BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=LETTER)
        styles = getSampleStyleSheet()

        story = []

        # TITLE PAGE
        story.append(Paragraph(f"<b><font size=24>{req.title}</font></b>", styles["Title"]))
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"<font size=14>Author: {req.author}</font>", styles["Normal"]))
        story.append(Spacer(1, 40))

        # CONTENTS
        story.append(Paragraph("<b>Table of Contents</b>", styles["Heading1"]))
        story.append(Spacer(1, 20))

        for i, sec in enumerate(req.sections, start=1):
            story.append(Paragraph(f"{i}. {sec.section_name}", styles["Normal"]))
        story.append(Spacer(1, 40))

        # SECTIONS
        for sec in req.sections:
            story.append(Paragraph(f"<b>{sec.section_name}</b>", styles["Heading1"]))
            story.append(Spacer(1, 15))

            # Image download
            try:
                img_data = requests.get(sec.image_url).content
                img_buffer = BytesIO(img_data)
                story.append(Image(img_buffer, width=400, height=250))
                story.append(Spacer(1, 15))
            except:
                pass  # if image fails, skip it

            story.append(Paragraph(sec.text.replace("\n", "<br/>"), styles["Normal"]))
            story.append(Spacer(1, 25))

        pdf.build(story)
        buffer.seek(0)

        return {
            "message": "PDF generated successfully.",
            "file": buffer.getvalue().hex()  # hex string for safe transfer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
