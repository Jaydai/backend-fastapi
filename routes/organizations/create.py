import logging

from fastapi import HTTPException, Request, status

from . import router

logger = logging.getLogger(__name__)


@router.post("", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def create_organization(request: Request) -> dict:
    logger.warning("Attempted to call unimplemented endpoint: POST /organizations")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Organization creation is not yet implemented"
    )
