# api/generate_images.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
import traceback

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ImageRequest(BaseModel):
    chapters: list[str]
    style: str = "modern illustration"

@router.post("/generate_images")
async def generate_images(req: ImageRequest):
    try:
        image_results = []

        for chapter in req.chapters:
            prompt = f"""
            Create a high-quality, clean, modern illustration representing the chapter:
            '{chapter}'.
            Style: {req.style}.
            White background. Professional. Ebook-friendly.
            """

            img = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size="1024x1024"
            )

            image_url = img.data[0].url
            image_results.append({"chapter": chapter, "image_url": image_url})

        return {"images": image_results}

    except Exception:
        print("ERROR in /generate_images:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")
