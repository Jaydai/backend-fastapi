import logging

from fastapi import HTTPException, Request, status

from dtos import InvitationResponseDTO
from services.invitation_service import InvitationService

from . import router

logger = logging.getLogger(__name__)


@router.get("/pending", response_model=list[InvitationResponseDTO], status_code=status.HTTP_200_OK)
async def get_pending_invitations(request: Request) -> list[InvitationResponseDTO]:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} getting pending invitations")

        invitations = InvitationService.get_pending_invitations(client, user_id)

        return invitations
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting pending invitations: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get pending invitations: {str(e)}")
