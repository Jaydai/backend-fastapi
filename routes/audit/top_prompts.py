"""Top prompts endpoint"""
from fastapi import HTTPException, Request, Query
from . import router
from dtos.audit_dto import TopPromptsWithContextDTO
from services.audit_service import AuditService
import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)


@router.get("/organizations/{organization_id}/top-prompts", response_model=TopPromptsWithContextDTO)
async def get_organization_top_prompts(
    request: Request,
    organization_id: str,
    start_date: Optional[str] = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back")
):
    """
    Get highest quality prompts for organization
    Includes top 10 prompts with content previews
    """
    start_time = time.time()
    logger.info(f"[AUDIT:top-prompts] Request started - org_id={organization_id}, start_date={start_date}, end_date={end_date}, days={days}")

    try:
        user_id = request.state.user_id
        logger.info(f"[AUDIT:top-prompts] User authenticated - user_id={user_id}")

        # TODO: Add permission check - verify user has admin/owner role in organization

        logger.info(f"[AUDIT:top-prompts] Calling AuditService.get_organization_top_prompts...")
        result = await AuditService.get_organization_top_prompts(
            request.state.supabase_client,
            user_id,
            organization_id,
            start_date,
            end_date,
            days
        )

        duration_ms = int((time.time() - start_time) * 1000)
        logger.info(f"[AUDIT:top-prompts] Request completed - org_id={organization_id}, duration={duration_ms}ms, has_data={result is not None}")

        return result

    except HTTPException:
        duration_ms = int((time.time() - start_time) * 1000)
        logger.warning(f"[AUDIT:top-prompts] HTTP exception - org_id={organization_id}, duration={duration_ms}ms")
        raise
    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)
        logger.error(f"[AUDIT:top-prompts] Error getting top prompts - org_id={organization_id}, duration={duration_ms}ms, error={str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get top prompts: {str(e)}")
