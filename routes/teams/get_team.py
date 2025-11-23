from fastapi import HTTPException, Request
import logging

from . import router
from services.team_service import TeamService
from dtos.team_dto import TeamDTO

logger = logging.getLogger(__name__)


@router.get("/{team_id}", response_model=TeamDTO)
async def get_team(request: Request, team_id: int) -> TeamDTO:
    """Get a specific team by ID"""
    try:
        team = TeamService.get_team_by_id(request.state.supabase_client, team_id)

        if not team:
            raise HTTPException(status_code=404, detail=f"Team {team_id} not found")

        return team

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching team {team_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch team: {str(e)}")
