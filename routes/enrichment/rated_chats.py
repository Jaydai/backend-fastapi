"""Rated chats endpoints"""
from fastapi import HTTPException, Request, Query
from . import router
from dtos.enrichment_dto import RatedChatDTO, OverrideQualityRequestDTO
from services.enrichment_service import EnrichmentService
import logging
from typing import Optional

logger = logging.getLogger(__name__)


@router.get("/rated-chats", response_model=list[RatedChatDTO])
async def get_rated_chats(
    request: Request,
    days: int = Query(default=30, ge=1, le=365),
    min_quality: Optional[float] = Query(default=None, ge=0, le=100),
    max_quality: Optional[float] = Query(default=None, ge=0, le=100),
    order_by: str = Query(default="quality_desc"),
    limit: int = Query(default=50, ge=1, le=200)
):
    """
    Get rated chats for the authenticated user
    """
    try:
        user_id = request.state.user_id
        results = EnrichmentService.get_rated_chats(
            request.state.supabase_client,
            user_id,
            days,
            min_quality,
            max_quality,
            order_by,
            limit
        )
        return results
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting rated chats: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get rated chats: {str(e)}")
