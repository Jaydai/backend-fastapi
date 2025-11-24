from fastapi import APIRouter

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])

# Not implemented yet (501)
from . import (  # noqa: E402
    get_status,
    update_status,
)
