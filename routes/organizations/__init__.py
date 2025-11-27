from fastapi import APIRouter

router = APIRouter(prefix="/organizations", tags=["Organizations"])

# Implemented endpoints
from . import (
    get_all,
    get_by_id,
    get_members,
    update_member_role,
    remove_member,
    get_invitations,
    get_templates,
    get_folders,
    get_version_content,
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
)
