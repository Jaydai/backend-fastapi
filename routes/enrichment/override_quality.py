"""Override quality score endpoint"""
from fastapi import HTTPException, Request
from . import router
from dtos.enrichment_dto import OverrideQualityRequestDTO
from services.enrichment_service import EnrichmentService
import logging

logger = logging.getLogger(__name__)


@router.post("/override-quality")
async def override_chat_quality(request: Request, dto: OverrideQualityRequestDTO):
    """
    Override chat quality score with user assessment
    """
    try:
        user_id = request.state.user_id
        success = EnrichmentService.override_chat_quality(
            request.state.supabase_client,
            user_id,
            dto.chat_provider_id,
            dto.quality_score
        )

        if not success:
            raise HTTPException(status_code=404, detail="Chat not found")

        return {"success": True, "message": "Quality score overridden successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error overriding quality: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to override quality: {str(e)}")
