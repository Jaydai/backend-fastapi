from fastapi import APIRouter

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


from . import root  # noqa: E402
