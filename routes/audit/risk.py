"""Risk statistics endpoint"""

import logging
import time

from fastapi import HTTPException, Query, Request

from dtos.audit_dto import RiskStatsWithContextDTO
from services.audit_service import AuditService

logger = logging.getLogger(__name__)


@router.get("/organizations/{organization_id}/risk", response_model=RiskStatsWithContextDTO)
async def get_organization_risk_stats(
    request: Request,
    organization_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
):
    """
    Get risk statistics for organization
    Includes risk levels, PII detection, and 7-day trend
    """
    start_time = time.time()
    logger.info(
        f"[AUDIT:risk] Request started - org_id={organization_id}, start_date={start_date}, end_date={end_date}, days={days}"
    )

    try:
        user_id = request.state.user_id
        logger.info(f"[AUDIT:risk] User authenticated - user_id={user_id}")

        # TODO: Add permission check - verify user has admin/owner role in organization

        logger.info("[AUDIT:risk] Calling AuditService.get_organization_risk_stats...")
        result = await AuditService.get_organization_risk_stats(
            request.state.supabase_client, user_id, organization_id, start_date, end_date, days
        )

        duration_ms = int((time.time() - start_time) * 1000)
        logger.info(
            f"[AUDIT:risk] Request completed - org_id={organization_id}, duration={duration_ms}ms, has_data={result is not None}"
        )

        return result

    except HTTPException:
        duration_ms = int((time.time() - start_time) * 1000)
        logger.warning(f"[AUDIT:risk] HTTP exception - org_id={organization_id}, duration={duration_ms}ms")
        raise
    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)
        logger.error(
            f"[AUDIT:risk] Error getting risk stats - org_id={organization_id}, duration={duration_ms}ms, error={str(e)}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=f"Failed to get risk stats: {str(e)}")
