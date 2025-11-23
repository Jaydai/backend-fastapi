from fastapi import HTTPException, Request
import logging

from . import router
from services.team_service import TeamService
from dtos.team_dto import AddTeamMemberRequestDTO, MemberAddedResponseDTO

logger = logging.getLogger(__name__)


@router.post("/{team_id}/members", response_model=MemberAddedResponseDTO)
async def add_team_member(
    request: Request,
    team_id: int,
    body: AddTeamMemberRequestDTO
) -> MemberAddedResponseDTO:
    """Add a user to a team"""
    try:
        member = TeamService.add_user_to_team(
            request.state.supabase_client,
            team_id,
            body.user_id,
            body.role
        )

        return MemberAddedResponseDTO(member=member)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error adding member to team {team_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add member: {str(e)}")
