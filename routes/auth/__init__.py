from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Implemented endpoints
from . import (
    sign_in,
    sign_up,
    sign_out,
    refresh,
    oauth_sign_in,
)

# Not implemented yet (501)
from . import (
    forgot_password,
    reset_password,
    me,
)
