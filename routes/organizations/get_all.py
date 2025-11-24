import logging

from fastapi import HTTPException, Request

from dtos import OrganizationResponseDTO
from services import OrganizationService

from . import router

logger = logging.getLogger(__name__)


@router.get("", response_model=list[OrganizationResponseDTO])
async def get_all(request: Request) -> list[OrganizationResponseDTO]:
    try:
        user_id = request.state.user_id  # Injected by middleware
        logger.info(f"User {user_id} fetching organizations")

        organizations = OrganizationService.get_organizations(request.state.supabase_client)

        logger.info(f"Returning {len(organizations)} organizations for user {user_id}")
        return organizations

    except Exception as e:
        logger.error(f"Error fetching organizations for user: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch organizations: {str(e)}")
