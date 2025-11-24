import logging

from fastapi import HTTPException, Query, Request, status

from dtos.stats_dto import UsageTimelineDTO
from services.stats_service import StatsService

from . import router

logger = logging.getLogger(__name__)


@router.get("/timeline", response_model=UsageTimelineDTO, status_code=status.HTTP_200_OK)
async def get_usage_timeline(
    request: Request,
    days: int = Query(30, description="Number of days to analyze", ge=1, le=365),
    granularity: str = Query("daily", description="Timeline granularity", regex="^(hourly|daily|weekly)$"),
) -> UsageTimelineDTO:
    """
    Get usage timeline data for charts with specified granularity.

    Parameters:
    - days: Number of days to analyze (1-365)
    - granularity: Time bucket size (hourly, daily, weekly)

    Returns:
    - Timeline data points with messages, chats, tokens, cost, and energy metrics
    - Aggregated by the specified granularity
    """
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} fetching usage timeline for {days} days with {granularity} granularity")

        # Service now returns DTO directly
        return StatsService.get_usage_timeline(client, user_id, days, granularity)

    except Exception as e:
        logger.error(f"Error getting usage timeline for {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get usage timeline: {str(e)}"
        )
