# api/generate_section.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
import traceback

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class GenerateSectionRequest(BaseModel):
    title: str
    prompt: str

@router.post("/generate_section")
async def generate_section(req: GenerateSectionRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You generate ebook sections."},
                {"role": "user", "content": req.prompt}
            ],
            max_tokens=1200
        )

        # FIXED: correct way to access message content
        content = response.choices[0].message.content

        return {
            "title": req.title,
            "section_text": content
        }

    except Exception as e:
        print("ERROR in /generate_section:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")
