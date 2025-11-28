import logging

from fastapi import HTTPException, Request, status

from . import router

logger = logging.getLogger(__name__)


@router.post("/forgot-password", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def forgot_password(request: Request) -> dict:
    logger.warning("Attempted to call unimplemented endpoint: POST /auth/forgot-password")
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Forgot password is not yet implemented")
