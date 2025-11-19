from fastapi import HTTPException, Request, status
import logging

from . import router

logger = logging.getLogger(__name__)


@router.delete("/{invitation_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def cancel_invitation(request: Request, invitation_id: str) -> dict:
    logger.warning(f"Attempted to call unimplemented endpoint: DELETE /invitations/{invitation_id}")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Cancel invitation is not yet implemented"
    )
