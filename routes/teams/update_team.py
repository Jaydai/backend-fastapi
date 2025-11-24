from fastapi import HTTPException, Request
import logging

from . import router
from services.team_service import TeamService
from dtos.team_dto import UpdateTeamRequestDTO, TeamUpdatedResponseDTO

logger = logging.getLogger(__name__)


@router.patch("/{team_id}", response_model=TeamUpdatedResponseDTO)
async def update_team(
    request: Request,
    team_id: str,
    body: UpdateTeamRequestDTO
) -> TeamUpdatedResponseDTO:
    """Update a team"""
    try:
        team = TeamService.update_team(
            request.state.supabase_client,
            team_id,
            body.name,
            body.description,
            body.parent_team_id,
            body.color
        )

        return TeamUpdatedResponseDTO(team=team)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating team {team_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update team: {str(e)}")
