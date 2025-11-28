import logging

from fastapi import HTTPException, Query, Request, status

from dtos.notification_dto import MarkAllReadResponseDTO, UpdateNotificationDTO
from services.notification_service import NotificationService

from . import router

logger = logging.getLogger(__name__)


@router.patch("", response_model=MarkAllReadResponseDTO, status_code=status.HTTP_200_OK)
async def mark_all_notifications_as_read(
    request: Request, mark_all_as_read: bool = Query(False)
) -> MarkAllReadResponseDTO:
    try:
        if not mark_all_as_read:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Query parameter 'mark_all_as_read=true' is required"
            )

        user_id = request.state.user_id
        logger.info(f"User {user_id} marking all notifications as read")

        result = NotificationService.mark_all_notifications_as_read(request.state.supabase_client, user_id)

        logger.info(f"User {user_id} marked {result.notifications_updated} notifications as read")
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking all notifications as read: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark all notifications as read: {str(e)}",
        )


@router.patch("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def mark_notification_as_read(request: Request, notification_id: int, update_data: UpdateNotificationDTO):
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} updating notification {notification_id}")

        if not update_data.read:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only marking as read is supported")

        success = NotificationService.mark_notification_as_read(request.state.supabase_client, notification_id, user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found or doesn't belong to user"
            )

        logger.info(f"User {user_id} marked notification {notification_id} as read")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking notification as read: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to mark notification as read: {str(e)}"
        )
