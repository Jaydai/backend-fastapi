from fastapi import APIRouter
from .auth import router as auth_router
from .permissions import router as permissions_router
from .examples import router as examples_router
from .org_examples import router as org_examples_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(permissions_router)
router.include_router(examples_router)
router.include_router(org_examples_router)

from . import root