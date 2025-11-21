from fastapi import HTTPException, Request, status
import logging

from . import router
from services import InvitationService
from dtos import InvitationResponseDTO, UpdateInvitationStatusDTO

logger = logging.getLogger(__name__)


@router.patch(
    "/{invitation_id}/status",
    response_model=InvitationResponseDTO,
    status_code=status.HTTP_200_OK
)
async def update_invitation_status(
    request: Request,
    invitation_id: str,
    update_data: UpdateInvitationStatusDTO
) -> InvitationResponseDTO:
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} updating invitation {invitation_id} to status {update_data.status}")

        invitation = InvitationService.update_invitation_status(
            request.state.supabase_client,
            invitation_id,
            user_id,
            update_data.status
        )

        logger.info(
            f"User {user_id} successfully updated invitation {invitation_id} "
            f"to status {update_data.status} for organization {invitation.organization_name}"
        )

        return invitation

    except ValueError as e:
        logger.warning(f"Failed to update invitation: {e}")
        error_message = str(e)

        if "not found" in error_message.lower():
            status_code = status.HTTP_404_NOT_FOUND
        elif "not for you" in error_message.lower() or "already a member" in error_message.lower():
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        raise HTTPException(
            status_code=status_code,
            detail=error_message
        )
    except Exception as e:
        logger.error(f"Error updating invitation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update invitation: {str(e)}"
        )
