"""Enrich single message endpoint"""
from fastapi import HTTPException, Request
from . import router
from dtos.enrichment_dto import EnrichMessageRequestDTO, EnrichMessageResponseDTO
from services.enrichment_service import EnrichmentService
import logging

logger = logging.getLogger(__name__)


@router.post("/enrich-message", response_model=EnrichMessageResponseDTO)
async def enrich_message(request: Request, dto: EnrichMessageRequestDTO):
    """
    Enrich a single message with risk assessment

    This endpoint can be called without authentication for batch processing scripts.
    """
    try:
        # Allow unauthenticated access for scripts - user_id will be None
        user_id = getattr(request.state, 'user_id', None)
        result = EnrichmentService.enrich_message(
            request.state.supabase_client,
            user_id,
            dto
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enriching message: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to enrich message: {str(e)}")
