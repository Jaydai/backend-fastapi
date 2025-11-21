"""Enrich single chat endpoint"""
from fastapi import HTTPException, Request
from . import router
from dtos.enrichment_dto import ChatEnrichmentRequestDTO, ChatEnrichmentResponseDTO
from services.enrichment_service import EnrichmentService
import logging

logger = logging.getLogger(__name__)


@router.post("/enrich-chat", response_model=ChatEnrichmentResponseDTO)
async def enrich_chat(request: Request, dto: ChatEnrichmentRequestDTO):
    """
    Enrich a single chat with classification and quality assessment
    """
    try:
        user_id = request.state.user_id
        result = EnrichmentService.enrich_chat(
            request.state.supabase_client,
            user_id,
            dto
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enriching chat: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to enrich chat: {str(e)}")
