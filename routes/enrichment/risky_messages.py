"""Risky messages endpoints"""
from fastapi import HTTPException, Request, Query
from . import router
from dtos.enrichment_dto import RiskyMessageDTO, WhitelistMessageRequestDTO
from services.enrichment_service import EnrichmentService
import logging

logger = logging.getLogger(__name__)


@router.get("/risky-messages", response_model=list[RiskyMessageDTO])
async def get_risky_messages(
    request: Request,
    days: int = Query(default=30, ge=1, le=365),
    min_risk_level: str = Query(default="medium"),
    limit: int = Query(default=50, ge=1, le=200)
):
    """
    Get risky messages for the authenticated user
    """
    try:
        user_id = request.state.user_id
        results = EnrichmentService.get_risky_messages(
            request.state.supabase_client,
            user_id,
            days,
            min_risk_level,
            limit
        )
        return results
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting risky messages: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get risky messages: {str(e)}")


@router.post("/whitelist-message")
async def whitelist_message(request: Request, dto: WhitelistMessageRequestDTO):
    """
    Mark a message as whitelisted (not risky)
    """
    try:
        user_id = request.state.user_id
        success = EnrichmentService.whitelist_message(
            request.state.supabase_client,
            user_id,
            dto.message_provider_id
        )

        if not success:
            raise HTTPException(status_code=404, detail="Message not found")

        return {"success": True, "message": "Message whitelisted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error whitelisting message: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to whitelist message: {str(e)}")
