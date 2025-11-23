from fastapi import HTTPException, Request
import logging

from . import router
from services.team_service import TeamService
from dtos.team_dto import OrganizationTeamsResponseDTO
from routes.dependencies import require_permission_in_organization
from domains.enums import PermissionEnum

logger = logging.getLogger(__name__)


@router.get("/organizations/{organization_id}", response_model=OrganizationTeamsResponseDTO)
@require_permission_in_organization(PermissionEnum.ORGANIZATION_READ)
async def get_organization_teams(
    request: Request,
    organization_id: str
) -> OrganizationTeamsResponseDTO:
    """Get all teams for an organization with tree structure"""
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} fetching teams for organization {organization_id}")

        teams = TeamService.get_organization_teams(
            request.state.supabase_client,
            organization_id
        )

        logger.info(f"Returning {teams.total_teams} teams for organization {organization_id}")
        return teams

    except Exception as e:
        logger.error(f"Error fetching teams for organization {organization_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch organization teams: {str(e)}"
        )
