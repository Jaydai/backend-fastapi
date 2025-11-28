import logging

from fastapi import HTTPException, Request, status

from services.notification_service import NotificationService

from . import router

logger = logging.getLogger(__name__)


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(request: Request, notification_id: int):
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} deleting notification {notification_id}")

        success = NotificationService.delete_notification(request.state.supabase_client, notification_id, user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found or doesn't belong to user"
            )

        logger.info(f"User {user_id} deleted notification {notification_id}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting notification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete notification: {str(e)}"
        )
