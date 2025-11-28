import logging

from fastapi import HTTPException, Request, status

from . import router

logger = logging.getLogger(__name__)


@router.delete("/{organization_id}/members/me", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def leave_organization(request: Request, organization_id: str) -> dict:
    logger.warning(f"Attempted to call unimplemented endpoint: DELETE /organizations/{organization_id}/members/me")
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Leave organization is not yet implemented")
