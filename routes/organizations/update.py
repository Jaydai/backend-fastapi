import logging

from fastapi import HTTPException, Request, status

from . import router

logger = logging.getLogger(__name__)


@router.put("/{organization_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def update_organization(request: Request, organization_id: str) -> dict:
    logger.warning(f"Attempted to call unimplemented endpoint: PUT /organizations/{organization_id}")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Organization update is not yet implemented"
    )
