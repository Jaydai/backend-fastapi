import logging

from fastapi import HTTPException, Request, status

from dtos import InvitationResponseDTO
from services.invitation_service import InvitationService

from . import router

logger = logging.getLogger(__name__)


@router.get(
    "/{invitation_id}",
    response_model=InvitationResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def get_invitation_by_id(request: Request, invitation_id: str) -> InvitationResponseDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} getting invitation {invitation_id}")

        invitation = InvitationService.get_invitation_by_id(client, invitation_id)

        if not invitation:
            raise HTTPException(status_code=404, detail="Invitation not found")

        return invitation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting invitation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get invitation: {str(e)}")
