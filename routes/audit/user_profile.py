"""User profile endpoint"""

import logging
import time

from fastapi import HTTPException, Query, Request

from dtos.audit_dto import UserProfileResponseDTO
from services.audit_service import AuditService

from . import router

logger = logging.getLogger(__name__)


@router.get("/organizations/{organization_id}/users/{user_id}", response_model=UserProfileResponseDTO)
async def get_user_profile(
    request: Request,
    organization_id: str,
    user_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
):
    """
    Get comprehensive profile for a specific user in the organization.
    Includes KPIs, activity timeline, provider breakdown, themes, and intents.
    Also includes comparison to organization averages.
    """
    start_time = time.time()
    logger.info(
        f"[AUDIT:user-profile] Request started - org_id={organization_id}, user_id={user_id}, "
        f"start_date={start_date}, end_date={end_date}, days={days}"
    )

    try:
        requesting_user_id = request.state.user_id
        logger.info(f"[AUDIT:user-profile] User authenticated - requesting_user_id={requesting_user_id}")

        # TODO: Add permission check - verify requesting user has admin/owner role in organization

        logger.info("[AUDIT:user-profile] Calling AuditService.get_user_profile...")
        result = await AuditService.get_user_profile(
            request.state.supabase_client,
            requesting_user_id,
            organization_id,
            user_id,
            start_date,
            end_date,
            days,
        )

        duration_ms = int((time.time() - start_time) * 1000)
        logger.info(
            f"[AUDIT:user-profile] Request completed - org_id={organization_id}, user_id={user_id}, "
            f"duration={duration_ms}ms, has_data={result is not None}"
        )

        return result

    except ValueError as e:
        duration_ms = int((time.time() - start_time) * 1000)
        logger.warning(
            f"[AUDIT:user-profile] Validation error - org_id={organization_id}, user_id={user_id}, "
            f"duration={duration_ms}ms, error={str(e)}"
        )
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        duration_ms = int((time.time() - start_time) * 1000)
        logger.warning(
            f"[AUDIT:user-profile] HTTP exception - org_id={organization_id}, user_id={user_id}, "
            f"duration={duration_ms}ms"
        )
        raise
    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)
        logger.error(
            f"[AUDIT:user-profile] Error getting user profile - org_id={organization_id}, user_id={user_id}, "
            f"duration={duration_ms}ms, error={str(e)}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=f"Failed to get user profile: {str(e)}")
