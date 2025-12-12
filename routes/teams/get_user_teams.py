"""
Route: GET /teams/user
Get all teams the current user belongs to
"""
import logging

from fastapi import Query, Request, status

from dtos.team_dto import TeamDTO
from services.team_service import TeamService

from . import router

logger = logging.getLogger(__name__)


@router.get("/user", response_model=list[TeamDTO], status_code=status.HTTP_200_OK)
async def get_user_teams(
    request: Request,
    organization_id: str | None = Query(None, description="Filter by organization ID"),
) -> list[TeamDTO]:
    """
    Get all teams the current user belongs to.

    Can optionally filter by organization_id to get teams within a specific organization.
    """
    client = request.state.supabase_client
    user_id = request.state.user_id

    logger.info(f"Fetching teams for user {user_id}, organization_id={organization_id}")

    teams = TeamService.get_user_teams(
        client=client,
        user_id=user_id,
        organization_id=organization_id,
    )

    logger.info(f"Returning {len(teams)} teams for user {user_id}")
    return teams
