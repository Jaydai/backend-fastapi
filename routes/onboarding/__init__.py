from fastapi import APIRouter

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])

from . import (  # noqa: E402
    chat,
    complete,
    get_flow,
    get_status,
    update_status,
    update_step,
    upload,
)
