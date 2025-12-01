# api/generate_full_ebook.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
import traceback
import httpx

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class FullEbookRequest(BaseModel):
    topic: str
    complexity: str = "medium"
    style: str = "modern illustration"

@router.post("/generate_full_ebook")
async def generate_full_ebook(req: FullEbookRequest):
    try:
        # 1. Generate outline
        outline_prompt = f"Create 10-15 ebook chapters about {req.topic}."
        outline_resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": outline_prompt}]
        )
        outline_text = outline_resp.choices[0].message.content
        chapters = [line.strip("-• ") for line in outline_text.split("\n") if line.strip()]

        # 2. Generate each chapter text
        chapter_contents = []
        for ch in chapters:
            sec_prompt = f"Write a detailed ebook chapter titled: '{ch}'. Topic: {req.topic}. Make it in-depth but easy to read."
            sec_resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": sec_prompt}],
                max_tokens=1500
            )
            chapter_contents.append({"chapter": ch, "text": sec_resp.choices[0].message.content})

        # 3. Generate images
        image_list = []
        for ch in chapters:
            img_prompt = f"Generate a modern illustration for chapter: {ch}."
            img = client.images.generate(
                model="gpt-image-1",
                prompt=img_prompt,
                size="1024x1024"
            )
            image_list.append({"chapter": ch, "image_url": img.data[0].url})

        return {
            "topic": req.topic,
            "chapters": chapter_contents,
            "images": image_list
        }

    except Exception:
        print("ERROR in /generate_full_ebook:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")
