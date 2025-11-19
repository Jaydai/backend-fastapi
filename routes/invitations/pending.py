from fastapi import HTTPException, Request, status
import logging

from . import router

logger = logging.getLogger(__name__)


@router.get("/pending", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def get_pending_invitations(request: Request) -> dict:
    logger.warning("Attempted to call unimplemented endpoint: GET /invitations/pending")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Get pending invitations is not yet implemented"
    )
