from fastapi import HTTPException, Request, status
import logging

from . import router
from services import InvitationService
from dtos import InvitationResponseDTO

logger = logging.getLogger(__name__)


@router.post(
    "/{invitation_id}/accept",
    response_model=InvitationResponseDTO,
    status_code=status.HTTP_200_OK
)
async def accept_invitation(
    request: Request,
    invitation_id: str
) -> InvitationResponseDTO:
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} accepting invitation {invitation_id}")

        invitation = InvitationService.accept_invitation(
            request.state.supabase_client,
            invitation_id,
            user_id
        )

        logger.info(
            f"User {user_id} successfully accepted invitation {invitation_id} "
            f"for organization {invitation.organization_name}"
        )

        return invitation

    except ValueError as e:
        logger.warning(f"Failed to accept invitation: {e}")
        error_message = str(e)

        # Map specific errors to appropriate status codes
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
        logger.error(f"Error accepting invitation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to accept invitation: {str(e)}"
        )
