"""Theme distribution endpoint for time-series analytics"""

import logging

from fastapi import HTTPException, Query, Request

from dtos.audit_dto import ThemeTimelineResponseDTO
from services.audit_timeseries_service import AuditTimeSeriesService

from . import router

logger = logging.getLogger(__name__)


@router.get("/organizations/{organization_id}/theme-distribution", response_model=ThemeTimelineResponseDTO)
async def get_theme_distribution(
    request: Request,
    organization_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    team_ids: list[str] | None = Query(default=None, description="Filter by team IDs"),
):
    """
    Get theme distribution for the date range
    Returns top themes and their current distribution
    """
    try:

        # TODO: Add permission check - verify user has admin/owner role in organization

        result = await AuditTimeSeriesService.get_theme_distribution(
            request.state.supabase_client, organization_id, start_date, end_date, days, team_ids or [], top_n=10
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting theme distribution: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get theme distribution: {str(e)}")
