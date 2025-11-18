from fastapi import APIRouter
from .auth import router as auth_router
from .templates import router as templates_router
from .organizations import router as organization_router
from .invitations import router as invitations_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(templates_router)
router.include_router(organization_router)
router.include_router(invitations_router)

from . import root