from fastapi import APIRouter

router = APIRouter(prefix="/templates", tags=["Templates"])

from . import get_all

# Import versions sub-router
from .versions import router as versions_router
router.include_router(versions_router)
