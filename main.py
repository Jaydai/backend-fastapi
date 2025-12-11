"""
Refactored main.py for Jaydai API
Clean, modular, and maintainable structure
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import config
from config.settings import settings
from middleware.auth_middleware import AuthenticationMiddleware
from middleware.locale_middleware import LocaleMiddleware

# Import main API router
from routes import router as api_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("test")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle application lifespan events.
    Manages startup and shutdown tasks.
    """
    # Startup
    logger.info("Starting up Jaydai API...")

    try:
        # TODO faire un call à chaque composant utilisé dans le BE (définit dans core/ (ou core/startup.py))

        # Test database connection
        from core.supabase import supabase

        supabase.storage.list_buckets()
        logger.info("Database connection verified")

    except Exception as e:
        logger.error(f"Startup verification failed: {str(e)}")

    logger.info(f"Jaydai API {settings.APP_VERSION} started successfully")

    # Application is running
    yield

    # Shutdown
    logger.info("Shutting down Jaydai API...")
    logger.info("Jaydai API shutdown completed")


# Create FastAPI application
app = FastAPI(
    title="Jaydai API",
    description="Clean and modular FastAPI backend for Jaydai",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "authorization", "content-type", "accept-language", "x-locale", "accept"],
    expose_headers=["*"],
)
app.add_middleware(AuthenticationMiddleware)
app.add_middleware(LocaleMiddleware)  # Automatically injects locale into request.state.locale

# Include main API router
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
