from fastapi import APIRouter

router = APIRouter(prefix="/api/teams", tags=["teams"])

# Import all route handlers
from . import (
    create_team,
    update_team,
    delete_team,
    get_team,
    get_organization_teams,
    get_team_members,
    add_team_member,
    remove_team_member,
    update_member_role
)
