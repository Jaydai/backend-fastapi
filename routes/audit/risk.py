"""Risk statistics endpoint"""
from fastapi import HTTPException, Request, Query
from . import router
from dtos.audit_dto import RiskStatsWithContextDTO
from services.audit_service import AuditService
import logging
from typing import Optional

logger = logging.getLogger(__name__)


@router.get("/organizations/{organization_id}/risk", response_model=RiskStatsWithContextDTO)
async def get_organization_risk_stats(
    request: Request,
    organization_id: str,
    start_date: Optional[str] = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back")
):
    """
    Get risk statistics for organization
    Includes risk levels, PII detection, and 7-day trend
    """
    try:
        user_id = request.state.user_id

        # TODO: Add permission check - verify user has admin/owner role in organization

        result = await AuditService.get_organization_risk_stats(
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
        logger.error(f"Error getting risk stats: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get risk stats: {str(e)}")
