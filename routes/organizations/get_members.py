import logging

from fastapi import HTTPException, Request

from domains.enums import PermissionEnum
from dtos import OrganizationMemberResponseDTO
from routes.dependencies import require_permission_in_organization
from services import OrganizationService

from . import router

logger = logging.getLogger(__name__)


@router.get("/{organization_id}/members", response_model=list[OrganizationMemberResponseDTO])
@require_permission_in_organization(PermissionEnum.ORGANIZATION_READ)
async def get_organization_members(request: Request, organization_id: str) -> list[OrganizationMemberResponseDTO]:
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} fetching members for organization {organization_id}")

        members = OrganizationService.get_organization_members(request.state.supabase_client, organization_id)

        logger.info(f"Returning {len(members)} members for organization {organization_id}")
        return members

    except Exception as e:
        logger.error(f"Error fetching members for organization {organization_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch organization members: {str(e)}")
