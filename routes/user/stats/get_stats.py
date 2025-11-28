import logging

from fastapi import HTTPException, Query, Request, status

from dtos.stats_dto import UserStatsDTO
from services.stats_service import StatsService

from . import router

logger = logging.getLogger(__name__)


@router.get("", response_model=UserStatsDTO, status_code=status.HTTP_200_OK)
async def get_user_stats(
    request: Request, recent_days: int = Query(7, description="Number of recent days to compare", ge=1, le=30)
) -> UserStatsDTO:
    """
    Get comprehensive user statistics including messages, chats, tokens, energy usage, and model usage.

    Returns statistics for all time with comparison to recent days period.
    """
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} fetching statistics with {recent_days} recent days")

        # Service now returns DTO directly
        return StatsService.get_user_stats(client, user_id, recent_days)

    except Exception as e:
        logger.error(f"Error getting user stats for {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get user statistics: {str(e)}"
        )
