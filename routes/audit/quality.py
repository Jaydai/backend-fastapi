"""Quality statistics endpoint"""

import logging
import time

from fastapi import HTTPException, Query, Request

from dtos.audit_dto import QualityStatsWithContextDTO
from services.audit_service import AuditService

from . import router

logger = logging.getLogger(__name__)


@router.get("/organizations/{organization_id}/quality", response_model=QualityStatsWithContextDTO)
async def get_organization_quality_stats(
    request: Request,
    organization_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
):
    """
    Get quality statistics for organization
    Includes average scores, distribution, and 7-day trend
    """
    start_time = time.time()
    logger.info(
        f"[AUDIT:quality] Request started - org_id={organization_id}, start_date={start_date}, end_date={end_date}, days={days}"
    )

    try:
        user_id = request.state.user_id
        logger.info(f"[AUDIT:quality] User authenticated - user_id={user_id}")

        # TODO: Add permission check - verify user has admin/owner role in organization

        logger.info("[AUDIT:quality] Calling AuditService.get_organization_quality_stats...")
        result = await AuditService.get_organization_quality_stats(
            request.state.supabase_client, user_id, organization_id, start_date, end_date, days
        )

        duration_ms = int((time.time() - start_time) * 1000)
        logger.info(
            f"[AUDIT:quality] Request completed - org_id={organization_id}, duration={duration_ms}ms, has_data={result is not None}"
        )

        return result

    except HTTPException:
        duration_ms = int((time.time() - start_time) * 1000)
        logger.warning(f"[AUDIT:quality] HTTP exception - org_id={organization_id}, duration={duration_ms}ms")
        raise
    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)
        logger.error(
            f"[AUDIT:quality] Error getting quality stats - org_id={organization_id}, duration={duration_ms}ms, error={str(e)}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=f"Failed to get quality stats: {str(e)}")
