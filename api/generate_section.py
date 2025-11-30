# api/generate_section.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai
import os

router = APIRouter()

# Load API key from environment (Vercel)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


class SectionRequest(BaseModel):
    title: str
    author: str
    section_name: str
    tone: str = "expert"


@router.post("/generate_section")
async def generate_section(req: SectionRequest):

    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="Missing OpenAI API key.")

    prompt = (
        f"Write a highly detailed, expert-level chapter titled '{req.section_name}' "
        f"for a premium ebook called '{req.title}' by {req.author}. "
        f"Tone: {req.tone}. "
        f"Include:\n"
        f"- Overview\n"
        f"- Key insights\n"
        f"- Actionable steps\n"
        f"- Advanced frameworks\n"
        f"- Example scenarios\n"
        f"- A Pro Tip box.\n"
        f"Write in a polished, engaging, premium ebook style.\n"
    )

    # GPT Response
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85,
    )

    chapter_text = response.choices[0].message["content"]

    # Image (Unsplash auto search)
    img_query = req.section_name.replace(" ", "+")
    image_url = f"https://source.unsplash.com/1200x800/?{img_query}"

    return {
        "section_name": req.section_name,
        "text": chapter_text,
        "image_url": image_url,
    }
