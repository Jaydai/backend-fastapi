import logging

from fastapi import HTTPException, Query, Request, status

from dtos.stats_dto import UsagePatternsDTO
from services.stats_service import StatsService

from . import router

logger = logging.getLogger(__name__)


@router.get("/patterns", response_model=UsagePatternsDTO, status_code=status.HTTP_200_OK)
async def get_usage_patterns(
    request: Request, days: int = Query(30, description="Number of days to analyze", ge=1, le=365)
) -> UsagePatternsDTO:
    """
    Get usage patterns showing when the user is most active.

    Returns:
    - Hourly distribution (messages per hour of day, 0-23)
    - Daily distribution (messages per day of week, Monday-Sunday)
    - Peak hour (most active hour)
    - Peak day (most active day)
    """
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} fetching usage patterns for {days} days")

        # Service now returns DTO directly
        return StatsService.get_usage_patterns(client, user_id, days)

    except Exception as e:
        logger.error(f"Error getting usage patterns for {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get usage patterns: {str(e)}"
        )
