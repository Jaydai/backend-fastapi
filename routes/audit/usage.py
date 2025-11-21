"""Usage statistics endpoint"""
from fastapi import HTTPException, Request, Query
from . import router
from dtos.audit_dto import UsageStatsWithContextDTO
from services.audit_service import AuditService
import logging
from typing import Optional

logger = logging.getLogger(__name__)


@router.get("/organizations/{organization_id}/usage", response_model=UsageStatsWithContextDTO)
async def get_organization_usage_stats(
    request: Request,
    organization_id: str,
    start_date: Optional[str] = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back")
):
    """
    Get usage statistics for organization
    Includes prompts, chats, active users, daily average, and 7-day trend
    """
    try:
        user_id = request.state.user_id

        # TODO: Add permission check - verify user has admin/owner role in organization

        result = await AuditService.get_organization_usage_stats(
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
        logger.error(f"Error getting usage stats: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get usage stats: {str(e)}")
