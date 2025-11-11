from fastapi import APIRouter
from .auth import router as auth_router
from .templates import router as templates_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(templates_router)

from . import root