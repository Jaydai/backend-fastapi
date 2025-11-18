from fastapi import HTTPException, Request, status
import logging

from . import router
from services import OrganizationService
from dtos import OrganizationDetailResponseDTO
from routes.dependencies import require_permission_in_organization
from domains.enums import PermissionEnum

logger = logging.getLogger(__name__)


@router.get(
    "/{organization_id}",
    response_model=OrganizationDetailResponseDTO
)
@require_permission_in_organization(PermissionEnum.ORGANIZATION_READ)
async def get_organization_by_id(
    request: Request,
    organization_id: str
) -> OrganizationDetailResponseDTO:
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} fetching details for organization {organization_id}")

        organization = OrganizationService.get_organization_by_id(
            request.state.supabase_client,
            organization_id
        )

        logger.info(
            f"Returning organization {organization_id} details with "
            f"{organization.members_count} members for user {user_id}"
        )

        return organization

    except ValueError as e:
        logger.warning(f"Organization not found or permission denied: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error fetching organization {organization_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch organization: {str(e)}"
        )
