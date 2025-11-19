from fastapi import APIRouter

router = APIRouter(prefix="/invitations", tags=["Invitations"])

from . import (
    pending,              # GET /pending
    update_status,        # PATCH /{id} - must be before get_by_id
    cancel,               # DELETE /{id}
    get_by_id,            # GET /{id} - must be last
)
