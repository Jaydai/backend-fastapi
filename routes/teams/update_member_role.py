import logging

from fastapi import HTTPException, Request

from dtos.team_dto import TeamMemberDTO, UpdateTeamMemberRoleRequestDTO
from services.team_service import TeamService

from . import router

logger = logging.getLogger(__name__)


@router.patch("/{team_id}/members/{user_id}", response_model=TeamMemberDTO)
async def update_member_role(
    request: Request, team_id: str, user_id: str, body: UpdateTeamMemberRoleRequestDTO
) -> TeamMemberDTO:
    """Update a team member's role"""
    try:
        member = TeamService.update_user_team_role(request.state.supabase_client, team_id, user_id, body.role)

        return member

    except Exception as e:
        logger.error(f"Error updating role for member {user_id} in team {team_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update member role: {str(e)}")
