import logging

from fastapi import HTTPException, Request, Response, status

from domains.enums import PermissionEnum
from routes.dependencies import require_permission_in_organization
from services import OrganizationService

from . import router

logger = logging.getLogger(__name__)


@router.delete("/{organization_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_permission_in_organization(PermissionEnum.ORGANIZATION_UPDATE)
async def remove_member(request: Request, organization_id: str, user_id: str) -> Response:
    try:
        requesting_user_id = request.state.user_id
        logger.info(f"User {requesting_user_id} removing user {user_id} from organization {organization_id}")

        # Remove the member
        OrganizationService.remove_member(request.state.supabase_client, organization_id, user_id)

        logger.info(f"Successfully removed user {user_id} from organization {organization_id}")

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        logger.warning(f"Failed to remove member: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error removing member: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to remove member: {str(e)}"
        )
