"""
POST /auth/verify-otp

Verifies OTP token_hash from email confirmation and returns session tokens.
"""

import logging

from fastapi import HTTPException, Response
from pydantic import BaseModel

from core.supabase import supabase
from domains.entities import Session
from utils import set_auth_cookies

from . import router

logger = logging.getLogger(__name__)


class VerifyOtpDTO(BaseModel):
    token_hash: str
    type: str  # 'signup' or 'email'


class VerifyOtpResponse(BaseModel):
    user_id: str
    email: str
    access_token: str
    refresh_token: str


@router.post("/verify-otp", response_model=VerifyOtpResponse)
async def verify_otp(data: VerifyOtpDTO, response: Response):
    """
    Verify OTP token_hash from email confirmation.

    This endpoint is called when a user clicks the email verification link
    that contains a token_hash parameter.
    """
    try:
        # Verify the OTP token_hash with Supabase
        verify_response = supabase.auth.verify_otp({
            "token_hash": data.token_hash,
            "type": data.type,
        })

        if not verify_response.session:
            logger.warning("[AUTH] No session returned from OTP verification")
            raise HTTPException(status_code=400, detail="Verification failed - no session")

        if not verify_response.user:
            logger.warning("[AUTH] No user returned from OTP verification")
            raise HTTPException(status_code=400, detail="Verification failed - no user")

        session = verify_response.session
        user = verify_response.user

        logger.info(f"[AUTH] OTP verification successful for user {user.id}")

        # Set auth cookies for the session
        auth_session = Session(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
        )
        set_auth_cookies(response, auth_session)

        return VerifyOtpResponse(
            user_id=user.id,
            email=user.email or "",
            access_token=session.access_token,
            refresh_token=session.refresh_token,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[AUTH] Error verifying OTP: {e}")
        raise HTTPException(status_code=400, detail=f"Verification failed: {str(e)}")
