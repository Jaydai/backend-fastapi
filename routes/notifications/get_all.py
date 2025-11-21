from fastapi import HTTPException, Request, status, Query
import logging

from . import router
from services.notification_service import NotificationService
from dtos.notification_dto import NotificationResponseDTO

logger = logging.getLogger(__name__)


@router.get("", response_model=list[NotificationResponseDTO], status_code=status.HTTP_200_OK)
async def get_all_notifications(
    request: Request,
    status_filter: str | None = Query(None, alias="status")
) -> list[NotificationResponseDTO]:
    try:
        user_id = request.state.user_id

        if status_filter == "unread":
            logger.info(f"User {user_id} getting unread notifications")
            notifications = NotificationService.get_unread_notifications(
                request.state.supabase_client,
                user_id
            )
        elif status_filter is None:
            logger.info(f"User {user_id} getting all notifications")
            notifications = NotificationService.get_all_notifications(
                request.state.supabase_client,
                user_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status filter: {status_filter}. Allowed: 'unread'"
            )

        logger.info(f"User {user_id} retrieved {len(notifications)} notifications")
        return notifications

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting notifications: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get notifications: {str(e)}"
        )
