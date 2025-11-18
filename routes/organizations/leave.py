from fastapi import HTTPException, Request, status
import logging

from . import router

logger = logging.getLogger(__name__)


@router.post("/{organization_id}/leave", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def leave_organization(request: Request, organization_id: str) -> dict:
    logger.warning(f"Attempted to call unimplemented endpoint: POST /organizations/{organization_id}/leave")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Leave organization is not yet implemented"
    )
