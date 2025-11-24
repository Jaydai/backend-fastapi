"""Adoption curve endpoint"""
from fastapi import HTTPException, Request, Query
from . import router
from dtos.audit_dto import AdoptionCurveResponseDTO
from services.audit_timeseries_service import AuditTimeSeriesService
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


@router.get("/organizations/{organization_id}/adoption-curve", response_model=AdoptionCurveResponseDTO)
async def get_adoption_curve(
    request: Request,
    organization_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    team_ids: List[str] | None = Query(default=None, description="Filter by team IDs"),
    granularity: str = Query(default="day", pattern="^(day|week|month)$", description="Time granularity")
):
    """
    Get adoption curve showing usage over time with optional team breakdown
    """
    try:
        result = await AuditTimeSeriesService.get_adoption_curve(
            request.state.supabase_client,
            organization_id,
            start_date,
            end_date,
            days,
            team_ids,
            granularity
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting adoption curve: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get adoption curve: {str(e)}")
