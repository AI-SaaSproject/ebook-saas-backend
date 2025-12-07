# api/generate_images.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
import traceback

router = APIRouter()

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

class ImageRequest(BaseModel):
    chapters: list[str]
    style: str = "realistic watercolor digital illustration"


@router.post("/generate_images")
async def generate_images(req: ImageRequest):
    if not STABILITY_API_KEY:
        raise HTTPException(status_code=500, detail="Missing STABILITY_API_KEY")

    try:
        image_results = []

        for chapter in req.chapters:
            prompt = f"""
            A {req.style} representing the chapter concept: '{chapter}'.
            High detail, soft lighting, realistic textures, 
            modern professional ebook aesthetic,
            no childish elements, no cartoon effects,
            relevant to the chapter’s meaning,
            clean white or subtle background.
            """

            # Stability API endpoint for SDXL
            url = "https://api.stability.ai/v1/generation/sdxl-1.0/text-to-image"

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {STABILITY_API_KEY}",
            }

            payload = {
                "text_prompts": [{"text": prompt}],
                "samples": 1,
                "width": 1024,
                "height": 1024,
                "cfg_scale": 7,   # quality + accuracy
                "steps": 30       # detail level
            }

            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=payload, headers=headers)

            if resp.status_code != 200:
                print("❌ Stability API Error:", resp.text)
                raise Exception("Image generation failed")

            data = resp.json()

            # Base64 image response
            img_base64 = data["artifacts"][0]["base64"]

            image_results.append({
                "chapter": chapter,
                "image_base64": img_base64
            })

        return {"images": image_results}

    except Exception:
        print("❌ ERROR in /generate_images:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")
