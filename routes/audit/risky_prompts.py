"""Risky prompts endpoint"""

import logging
import time

from fastapi import HTTPException, Query, Request

from dtos.audit_dto import RiskyPromptsWithContextDTO
from services.audit_service import AuditService

from . import router

logger = logging.getLogger(__name__)


@router.get("/organizations/{organization_id}/risky-prompts", response_model=RiskyPromptsWithContextDTO)
async def get_organization_risky_prompts(
    request: Request,
    organization_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
):
    """
    Get highest risk prompts for organization
    Includes top 10 risky prompts with risk details
    """
    start_time = time.time()
    logger.info(
        f"[AUDIT:risky-prompts] Request started - org_id={organization_id}, start_date={start_date}, end_date={end_date}, days={days}"
    )

    try:
        user_id = request.state.user_id
        logger.info(f"[AUDIT:risky-prompts] User authenticated - user_id={user_id}")

        # TODO: Add permission check - verify user has admin/owner role in organization

        logger.info("[AUDIT:risky-prompts] Calling AuditService.get_organization_risky_prompts...")
        result = await AuditService.get_organization_risky_prompts(
            request.state.supabase_client, user_id, organization_id, start_date, end_date, days
        )

        duration_ms = int((time.time() - start_time) * 1000)
        logger.info(
            f"[AUDIT:risky-prompts] Request completed - org_id={organization_id}, duration={duration_ms}ms, has_data={result is not None}"
        )

        return result

    except HTTPException:
        duration_ms = int((time.time() - start_time) * 1000)
        logger.warning(f"[AUDIT:risky-prompts] HTTP exception - org_id={organization_id}, duration={duration_ms}ms")
        raise
    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)
        logger.error(
            f"[AUDIT:risky-prompts] Error getting risky prompts - org_id={organization_id}, duration={duration_ms}ms, error={str(e)}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=f"Failed to get risky prompts: {str(e)}")
