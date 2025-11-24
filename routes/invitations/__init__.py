from fastapi import APIRouter

router = APIRouter(prefix="/invitations", tags=["Invitations"])

from . import (  # noqa: E402
    cancel,  # DELETE /{id}
    get_by_id,  # GET /{id} - must be last
    pending,  # GET /pending
    update_status,  # PATCH /{id} - must be before get_by_id
)
