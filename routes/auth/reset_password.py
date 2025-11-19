from fastapi import HTTPException, Request, status
import logging

from . import router

logger = logging.getLogger(__name__)


@router.post("/reset-password", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def reset_password(request: Request) -> dict:
    logger.warning("Attempted to call unimplemented endpoint: POST /auth/reset-password")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Reset password is not yet implemented"
    )
