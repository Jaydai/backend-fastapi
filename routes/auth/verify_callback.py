"""
POST /auth/verify-callback

Verifies tokens from email confirmation callback and returns user info.
"""

import logging

from fastapi import HTTPException, Response
from pydantic import BaseModel

from core.supabase import supabase
from utils import set_auth_cookies

from . import router

logger = logging.getLogger(__name__)


class VerifyCallbackDTO(BaseModel):
    access_token: str
    refresh_token: str


class VerifyCallbackResponse(BaseModel):
    user_id: str
    email: str
    email_confirmed: bool


@router.post("/verify-callback", response_model=VerifyCallbackResponse)
async def verify_callback(data: VerifyCallbackDTO, response: Response):
    """
    Verify tokens from email confirmation callback.

    This endpoint is called after Supabase redirects the user back to our app
    with tokens in the URL. It verifies the tokens and sets auth cookies.
    """
    try:
        # Verify the access token by getting the user
        user_response = supabase.auth.get_user(data.access_token)

        if not user_response.user:
            logger.warning("[AUTH] Invalid access token in callback")
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user = user_response.user

        # Check if email is confirmed
        email_confirmed = user.email_confirmed_at is not None

        if not email_confirmed:
            logger.warning(f"[AUTH] Email not confirmed for user {user.id}")
            # Still allow proceeding - the token is valid, email will be marked confirmed

        logger.info(f"[AUTH] Email verification successful for user {user.id}")

        # Set auth cookies for the session
        from domains.entities import Session

        session = Session(
            access_token=data.access_token,
            refresh_token=data.refresh_token,
        )
        set_auth_cookies(response, session)

        return VerifyCallbackResponse(
            user_id=user.id,
            email=user.email or "",
            email_confirmed=email_confirmed,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[AUTH] Error verifying callback: {e}")
        raise HTTPException(status_code=500, detail="Failed to verify email")
