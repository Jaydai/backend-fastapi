import logging

from fastapi import HTTPException, Request, status

from dtos.notification_dto import NotificationStatsResponseDTO
from services.notification_service import NotificationService

from . import router

logger = logging.getLogger(__name__)


@router.get("/stats", response_model=NotificationStatsResponseDTO, status_code=status.HTTP_200_OK)
async def get_notification_stats(request: Request) -> NotificationStatsResponseDTO:
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} getting notification stats")

        stats = NotificationService.get_notification_stats(request.state.supabase_client, user_id)

        logger.info(f"User {user_id} has {stats.total} total, {stats.unread} unread notifications")
        return stats

    except Exception as e:
        logger.error(f"Error getting notification stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get notification stats: {str(e)}"
        )
