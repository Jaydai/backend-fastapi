from fastapi import HTTPException, Request, status
import logging

from . import router

logger = logging.getLogger(__name__)


@router.get("/{invitation_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def get_invitation_by_id(request: Request, invitation_id: str) -> dict:
    logger.warning(f"Attempted to call unimplemented endpoint: GET /invitations/{invitation_id}")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Get invitation details is not yet implemented"
    )
