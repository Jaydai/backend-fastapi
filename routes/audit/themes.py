"""Theme statistics endpoint"""
from fastapi import HTTPException, Request, Query
from . import router
from dtos.audit_dto import ThemeStatsWithContextDTO
from services.audit_service import AuditService
import logging
from typing import Optional

logger = logging.getLogger(__name__)


@router.get("/organizations/{organization_id}/themes", response_model=ThemeStatsWithContextDTO)
async def get_organization_theme_stats(
    request: Request,
    organization_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back")
):
    """
    Get theme distribution statistics for organization
    Includes top themes with counts and percentages
    """
    try:
        user_id = request.state.user_id

        # TODO: Add permission check - verify user has admin/owner role in organization

        result = await AuditService.get_organization_theme_stats(
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
        logger.error(f"Error getting theme stats: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get theme stats: {str(e)}")
