import logging

from fastapi import HTTPException, Request, status

from . import router

logger = logging.getLogger(__name__)


@router.get("/metadata", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def get_user_metadata(request: Request) -> dict:
    logger.warning("Attempted to call unimplemented endpoint: GET /user/metadata")
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Get user metadata is not yet implemented")
