# api/config.py

import os
from dotenv import load_dotenv

# load .env if running locally (Vercel also injects env automatically)
load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

settings = Settings()
