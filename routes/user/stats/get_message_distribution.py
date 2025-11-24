import logging

from fastapi import HTTPException, Request, status

from dtos.stats_dto import MessageDistributionDTO
from services.stats_service import StatsService

from . import router

logger = logging.getLogger(__name__)


@router.get("/messages/distribution", response_model=MessageDistributionDTO, status_code=status.HTTP_200_OK)
async def get_message_distribution(request: Request) -> MessageDistributionDTO:
    """
    Get message distribution statistics by role and model.

    Returns:
    - Distribution of messages by role (user, assistant, system)
    - Distribution of messages by model (gpt-4, claude-3, etc.)
    - Total message count
    """
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} fetching message distribution")

        # Service now returns DTO directly
        return StatsService.get_message_distribution(client, user_id)

    except Exception as e:
        logger.error(f"Error getting message distribution for {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get message distribution: {str(e)}"
        )
