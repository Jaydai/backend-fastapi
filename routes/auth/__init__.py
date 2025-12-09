from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Implemented endpoints
from . import (  # noqa: E402
    forgot_password,
    oauth_sign_in,
    refresh,
    reset_password,
    sign_in,
    sign_out,
    sign_up,
    verify_callback,
)
