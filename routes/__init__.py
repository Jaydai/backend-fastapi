from fastapi import APIRouter
from .auth import router as auth_router
from .prompts import router as prompts_router
from .organizations import router as organization_router
from .invitations import router as invitations_router
from .users import router as users_router
from .enrichment import router as enrichment_router
from .audit import router as audit_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(prompts_router)
router.include_router(organization_router)
router.include_router(invitations_router)
router.include_router(users_router)
router.include_router(enrichment_router, prefix="/enrichment", tags=["enrichment"])
router.include_router(audit_router, prefix="/audit", tags=["audit"])

from . import root