from fastapi import HTTPException, Request, status
import logging

from . import router

logger = logging.getLogger(__name__)


@router.put("/metadata", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def update_user_metadata(request: Request) -> dict:
    logger.warning("Attempted to call unimplemented endpoint: PUT /user/metadata")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Update user metadata is not yet implemented"
    )
