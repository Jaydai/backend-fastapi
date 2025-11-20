from fastapi import APIRouter
from .auth import router as auth_router
from .prompts import router as prompts_router
from .organizations import router as organization_router
from .invitations import router as invitations_router
from .users import router as users_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(prompts_router)
router.include_router(organization_router)
router.include_router(invitations_router)
router.include_router(users_router)

from . import root