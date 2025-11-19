from fastapi import Request, status, HTTPException, Query
import logging

from . import router
from services.stats_service import StatsService
from dtos.stats_dto import UsageOverviewDTO

logger = logging.getLogger(__name__)


@router.get("/overview", response_model=UsageOverviewDTO, status_code=status.HTTP_200_OK)
async def get_usage_overview(
    request: Request,
    days: int = Query(30, description="Number of days to analyze", ge=1, le=365)
) -> UsageOverviewDTO:
    """
    Get comprehensive usage overview for the specified time period.

    Returns:
    - Period information (days, start_date, end_date)
    - Summary metrics (messages, chats, tokens, cost, energy, CO2)
    - Model breakdown (usage per model)
    - Provider breakdown (usage per AI provider)
    - Chat statistics
    """
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} fetching usage overview for {days} days")

        # Service now returns DTO directly
        return StatsService.get_usage_overview(client, user_id, days)

    except Exception as e:
        logger.error(f"Error getting usage overview for {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get usage overview: {str(e)}"
        )
