from fastapi import HTTPException, Request, status
import logging

from . import router

logger = logging.getLogger(__name__)


@router.get("/me", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def get_current_user(request: Request) -> dict:
    logger.warning("Attempted to call unimplemented endpoint: GET /auth/me")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Get current user is not yet implemented"
    )
