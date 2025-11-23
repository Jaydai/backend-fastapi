from fastapi import HTTPException, Request
import logging

from . import router
from services.team_service import TeamService
from dtos.team_dto import TeamDeletedResponseDTO

logger = logging.getLogger(__name__)


@router.delete("/{team_id}", response_model=TeamDeletedResponseDTO)
async def delete_team(request: Request, team_id: int) -> TeamDeletedResponseDTO:
    """Delete a team"""
    try:
        TeamService.delete_team(request.state.supabase_client, team_id)
        return TeamDeletedResponseDTO(team_id=team_id)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting team {team_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete team: {str(e)}")
