from fastapi import Request, status, HTTPException, Query
import logging

from . import router
from services.stats_service import StatsService
from dtos.stats_dto import WeeklyConversationStatsDTO

logger = logging.getLogger(__name__)


@router.get("/chats/weekly", response_model=WeeklyConversationStatsDTO, status_code=status.HTTP_200_OK)
async def get_weekly_chat_stats(
    request: Request,
    days: int = Query(7, description="Number of days to analyze", ge=1, le=30)
) -> WeeklyConversationStatsDTO:
    """
    Get chat statistics with daily breakdown for the specified period.

    Returns:
    - Total conversations and messages in the period
    - Daily breakdown of conversations and messages
    """
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} fetching chat statistics for {days} days")

        # Service now returns DTO directly
        return StatsService.get_weekly_conversation_stats(client, user_id, days)

    except Exception as e:
        logger.error(f"Error getting weekly chat stats for {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get weekly chat statistics: {str(e)}"
        )
