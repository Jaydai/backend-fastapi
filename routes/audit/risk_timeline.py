"""Risk timeline endpoint"""

import logging

from fastapi import HTTPException, Query, Request

from dtos.audit_dto import RiskTimelineResponseDTO
from services.audit_timeseries_service import AuditTimeSeriesService

from . import router

logger = logging.getLogger(__name__)


@router.get("/organizations/{organization_id}/risk-timeline", response_model=RiskTimelineResponseDTO)
async def get_risk_timeline(
    request: Request,
    organization_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    team_ids: list[str] | None = Query(default=None, description="Filter by team IDs"),
    granularity: str = Query(default="day", pattern="^(day|week|month)$", description="Time granularity"),
):
    """
    Get risk timeline showing risky messages over time with breakdown by risk type
    """
    try:
        result = await AuditTimeSeriesService.get_risk_timeline(
            request.state.supabase_client, organization_id, start_date, end_date, days, team_ids, granularity
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting risk timeline: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get risk timeline: {str(e)}")
