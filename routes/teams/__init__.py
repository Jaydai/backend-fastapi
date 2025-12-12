from fastapi import APIRouter

router = APIRouter(prefix="/teams", tags=["teams"])

# Import all route handlers
from . import (  # noqa: E402
    add_team_member,
    create_team,
    delete_team,
    get_organization_teams,
    get_user_teams,  # /user must come before /{team_id}
    get_team,
    get_team_members,
    remove_team_member,
    update_member_role,
    update_team,
)
