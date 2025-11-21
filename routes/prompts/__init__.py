from fastapi import APIRouter

router = APIRouter(prefix="/prompts", tags=["Prompts"])

# Import sub-routers
from ..templates import router as templates_router

# Include templates router (will be at /prompts/templates)
router.include_router(templates_router)
