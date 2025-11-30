"""
Root FastAPI app for Ebook SaaS Backend.
This file wires up routes and provides health/readiness endpoints.
Do NOT put your OPENAI_API_KEY here — add it in Vercel env vars.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import routers
from api.generate_section import router as generate_router
from api.compile_pdf import router as pdf_router

app = FastAPI(
    title="Ebook SaaS Backend",
    description="Premium ebook generator API (text + images + PDF exports)",
    version="1.0.0",
)

# CORS - allow your Lovable frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routes (files will be added next)
app.include_router(generate_router, prefix="", tags=["generation"])
app.include_router(pdf_router, prefix="", tags=["export"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "ebook-saas-backend"}

@app.get("/")
def root():
    return {
        "message": "Ebook SaaS Backend API is running.",
        "version": app.version
    }
