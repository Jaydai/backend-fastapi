from fastapi import HTTPException, Request, status
import logging

from . import router
from services import OrganizationService
from dtos import UpdateMemberRoleDTO, OrganizationMemberResponseDTO
from routes.dependencies import require_permission_in_organization
from domains.enums import PermissionEnum

logger = logging.getLogger(__name__)


@router.patch(
    "/{organization_id}/members/{user_id}/role",
    response_model=OrganizationMemberResponseDTO,
    status_code=status.HTTP_200_OK
)
@require_permission_in_organization(PermissionEnum.ORGANIZATION_UPDATE)
async def update_member_role(
    request: Request,
    organization_id: str,
    user_id: str,
    update_data: UpdateMemberRoleDTO
) -> OrganizationMemberResponseDTO:
    try:
        requesting_user_id = request.state.user_id
        logger.info(
            f"User {requesting_user_id} updating role for user {user_id} "
            f"in organization {organization_id} to {update_data.role}"
        )

        updated_member: OrganizationMemberResponseDTO = OrganizationService.update_member_role(
            request.state.supabase_client,
            organization_id,
            user_id,
            update_data.role
        )

        logger.info(
            f"Successfully updated role for user {user_id} "
            f"in organization {organization_id} to {update_data.role}"
        )

        return updated_member

    except ValueError as e:
        logger.warning(f"Failed to update member role: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating member role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update member role: {str(e)}"
        )
