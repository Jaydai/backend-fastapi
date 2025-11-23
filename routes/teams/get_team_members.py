from fastapi import HTTPException, Request
import logging

from . import router
from services.team_service import TeamService
from dtos.team_dto import TeamMemberDTO

logger = logging.getLogger(__name__)


@router.get("/{team_id}/members", response_model=list[TeamMemberDTO])
async def get_team_members(request: Request, team_id: int) -> list[TeamMemberDTO]:
    """Get all members of a team"""
    try:
        members = TeamService.get_team_members(request.state.supabase_client, team_id)
        return members

    except Exception as e:
        logger.error(f"Error fetching members for team {team_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch team members: {str(e)}")
