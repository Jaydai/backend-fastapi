import logging

from fastapi import HTTPException, Request, status

from . import router

logger = logging.getLogger(__name__)


@router.post("/{organization_id}/invitations", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def invite_member(request: Request, organization_id: str) -> dict:
    logger.warning(f"Attempted to call unimplemented endpoint: POST /organizations/{organization_id}/invitations")
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Member invitation is not yet implemented")
