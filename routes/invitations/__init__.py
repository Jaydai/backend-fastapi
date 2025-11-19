from fastapi import APIRouter

router = APIRouter(prefix="/invitations", tags=["Invitations"])

# Implemented endpoints
from . import (
    accept,
    decline,
)

# Not implemented yet (501)
from . import (
    pending,
    get_by_id,
    cancel,
)
