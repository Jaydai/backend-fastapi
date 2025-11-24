"""Risky prompts endpoint"""
from fastapi import HTTPException, Request, Query
from . import router
from dtos.audit_dto import RiskyPromptsWithContextDTO
from services.audit_service import AuditService
import logging
from typing import Optional

logger = logging.getLogger(__name__)


@router.get("/organizations/{organization_id}/risky-prompts", response_model=RiskyPromptsWithContextDTO)
async def get_organization_risky_prompts(
    request: Request,
    organization_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back")
):
    """
    Get highest risk prompts for organization
    Includes top 10 risky prompts with risk details
    """
    try:
        user_id = request.state.user_id

        # TODO: Add permission check - verify user has admin/owner role in organization

        result = await AuditService.get_organization_risky_prompts(
            request.state.supabase_client,
            user_id,
            organization_id,
            start_date,
            end_date,
            days
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting risky prompts: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get risky prompts: {str(e)}")
