import os
from config import settings
from . import router

@router.get("/")
async def root():
    """Root endpoint - API status"""
    return {
        "message": "Welcome to Jaydai API",
        "version": settings.APP_VERSION,
        "status": "running",
        "environment": os.getenv("ENVIRONMENT")
    }