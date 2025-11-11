from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])

from . import (
    sign_in,
    sign_up,
    sign_out,
    refresh,
    # forgot_password,
    # reset_password,
    # verify_email,
    # confirm,
    # confirm_supabase,
    # me,
    # get_workspace_role,
    # sign_in_with_google,
    # linkedin_authorize,
    # linkedin_callback,
)
