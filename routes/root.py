import os

from fastapi import APIRouter

from config import settings

router = APIRouter()



@router.get("/")
async def root():
    """Root endpoint - API status"""
    return {
        "message": "Welcome to Jaydai API",
        "version": settings.APP_VERSION,
        "status": "running",
        "environment": os.getenv("ENVIRONMENT"),
        "supabase_url": os.getenv("SUPABASE_URL"),
    }
