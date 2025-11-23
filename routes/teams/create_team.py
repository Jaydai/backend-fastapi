from fastapi import HTTPException, Request
import logging

from . import router
from services.team_service import TeamService
from dtos.team_dto import CreateTeamRequestDTO, TeamCreatedResponseDTO
from routes.dependencies import require_permission_in_organization
from domains.enums import PermissionEnum

logger = logging.getLogger(__name__)


@router.post("/organizations/{organization_id}", response_model=TeamCreatedResponseDTO)
@require_permission_in_organization(PermissionEnum.ORGANIZATION_UPDATE)
async def create_team(
    request: Request,
    organization_id: str,
    body: CreateTeamRequestDTO
) -> TeamCreatedResponseDTO:
    """Create a new team in an organization"""
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} creating team '{body.name}' in organization {organization_id}")

        team = TeamService.create_team(
            request.state.supabase_client,
            organization_id,
            body.name,
            body.description,
            body.parent_team_id,
            body.color
        )

        logger.info(f"Team {team.id} created successfully")
        return TeamCreatedResponseDTO(team=team)

    except ValueError as e:
        logger.warning(f"Validation error creating team: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating team: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create team: {str(e)}"
        )
