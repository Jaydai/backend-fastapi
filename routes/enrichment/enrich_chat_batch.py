"""Enrich multiple chats endpoint"""
from fastapi import HTTPException, Request
from . import router
from dtos.enrichment_dto import ChatEnrichmentBatchRequestDTO
from services.enrichment_service import EnrichmentService
import logging

logger = logging.getLogger(__name__)


@router.post("/enrich-chat-batch")
async def enrich_chat_batch(request: Request, dto: ChatEnrichmentBatchRequestDTO):
    """
    Enrich multiple chats in parallel (1-50 chats)
    Returns list of results with success/error indicators
    """
    try:
        user_id = request.state.user_id
        results = await EnrichmentService.enrich_chat_batch(
            request.state.supabase_client,
            user_id,
            dto.chats
        )
        return {"results": results}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enriching chat batch: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to enrich chat batch: {str(e)}")
