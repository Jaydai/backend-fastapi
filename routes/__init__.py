from fastapi import APIRouter

from .auth import router as auth_router
from .root import router as root_router
from .templates import router as templates_router
from .folders import router as folders_router
from .blocks import router as blocks_router
from .organizations import router as organization_router
from .invitations import router as invitations_router
from .user import router as user_router
from .onboarding import router as onboarding_router
from .messages import router as messages_router
from .chats import router as chats_router
from .batch import router as batch_router
from .notifications import router as notifications_router
from .enrichment import router as enrichment_router
from .audit import router as audit_router
from .teams import router as teams_router


router = APIRouter()
router.include_router(auth_router)
router.include_router(templates_router)
router.include_router(folders_router)
router.include_router(blocks_router)
router.include_router(organization_router)
router.include_router(invitations_router)
router.include_router(user_router)
router.include_router(onboarding_router)
router.include_router(messages_router)
router.include_router(chats_router)
router.include_router(batch_router)
router.include_router(notifications_router)
router.include_router(enrichment_router, prefix="/enrichment", tags=["enrichment"])
router.include_router(audit_router, prefix="/audit", tags=["audit"])
router.include_router(teams_router)


from . import root
