"""Enrich multiple messages endpoint"""
from fastapi import HTTPException, Request
from . import router
from dtos.enrichment_dto import EnrichMessageBatchRequestDTO
from services.enrichment_service import EnrichmentService
import logging

logger = logging.getLogger(__name__)


@router.post("/enrich-message-batch")
async def enrich_message_batch(request: Request, dto: EnrichMessageBatchRequestDTO):
    """
    Enrich multiple messages with risk assessment (1-100 messages)
    Returns list of results with success/error indicators

    This endpoint can be called without authentication for batch processing scripts.
    """

    try:
        # Allow unauthenticated access for scripts - user_id will be None
        user_id = getattr(request.state, 'user_id', None)
        results = EnrichmentService.enrich_message_batch(
            request.state.supabase_client,
            user_id,
            dto.messages
        )
        return {"results": results}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enriching message batch: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to enrich message batch: {str(e)}")
