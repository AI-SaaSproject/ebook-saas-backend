# api/generate_outline.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
import traceback

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OutlineRequest(BaseModel):
    topic: str
    complexity: str = "medium"  # short, medium, long

@router.post("/generate_outline")
async def generate_outline(req: OutlineRequest):
    try:
        prompt = f"""
        Create a chapter outline for an ebook about: {req.topic}.

        Complexity level: {req.complexity}.

        Requirements:
        - 8 to 15 chapters depending on complexity.
        - Use short, clear chapter titles.
        - Make it engaging and logically structured.
        - Return ONLY a Python list of chapter titles.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        text = response.choices[0].message.content

        # Convert bullet points into a list
        lines = [line.strip("-• ") for line in text.split("\n") if line.strip()]
        return {"outline": lines}

    except Exception:
        print("ERROR in /generate_outline:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")
