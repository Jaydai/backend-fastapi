from fastapi import APIRouter

router = APIRouter(prefix="/organizations", tags=["Organizations"])

# Implemented endpoints
# Not implemented yet (501)
from . import (  # noqa: E402
    create,
    delete,
    get_all,
    get_by_id,
    get_invitations,
    get_templates,
    get_folders,
    get_user_role,
    get_ai_coach_insights,
)

# Not implemented yet (501)
from . import (
    create,
    update,
    delete,
    invite_member,
    leave,
    remove_member,
    update,
    update_member_role,
)
