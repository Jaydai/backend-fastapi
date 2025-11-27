import logging

from fastapi import HTTPException, Request, status

from services.invitation_service import InvitationService

from . import router

logger = logging.getLogger(__name__)


@router.delete("/{invitation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_invitation(request: Request, invitation_id: str):
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} cancelling invitation {invitation_id}")

        success = InvitationService.cancel_invitation(client, invitation_id, user_id)

        if not success:
            raise HTTPException(status_code=404, detail="Invitation not found")

        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling invitation: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to cancel invitation: {str(e)}"
        )
