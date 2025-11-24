from fastapi import HTTPException, Request
import logging

from . import router
from services.team_service import TeamService
from dtos.team_dto import MemberRemovedResponseDTO

logger = logging.getLogger(__name__)


@router.delete("/{team_id}/members/{user_id}", response_model=MemberRemovedResponseDTO)
async def remove_team_member(
    request: Request,
    team_id: str,
    user_id: str
) -> MemberRemovedResponseDTO:
    """Remove a user from a team"""
    try:
        TeamService.remove_user_from_team(request.state.supabase_client, team_id, user_id)
        return MemberRemovedResponseDTO(user_id=user_id, team_id=team_id)

    except Exception as e:
        logger.error(f"Error removing member {user_id} from team {team_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to remove member: {str(e)}")
