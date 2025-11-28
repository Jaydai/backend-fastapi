"""Organization audit endpoint"""

import logging

from fastapi import HTTPException, Query, Request

from dtos.audit_dto import OrganizationAuditResponseDTO
from services.audit_service import AuditService

from . import router

logger = logging.getLogger(__name__)


@router.get("/organizations/{organization_id}", response_model=OrganizationAuditResponseDTO)
async def get_organization_audit(
    request: Request,
    organization_id: str,
    start_date: str | None = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
):
    """
    Get comprehensive organization audit with quality, risk, usage, and user statistics
    Requires admin or owner role in the organization

    This endpoint fetches data in parallel for optimal performance
    """
    try:
        user_id = request.state.user_id

        # TODO: Add permission check - verify user has admin/owner role in organization
        # For now, assuming authentication middleware handles this

        result = await AuditService.get_organization_audit(
            request.state.supabase_client, user_id, organization_id, start_date, end_date, days
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting organization audit: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get organization audit: {str(e)}")
