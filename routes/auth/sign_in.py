"""Sign in endpoint"""
from fastapi import HTTPException, Request, Response
from . import router
from dtos import SignInDTO
import logging
from services import AuthService
from domains.entities import Session

logger = logging.getLogger(__name__)


@router.post("/sign_in")
async def sign_in(sign_in_dto: SignInDTO, request: Request, response: Response):
    try:
        session: Session = AuthService.sign_in_with_password(sign_in_dto)

        client_type = request.headers.get("X-Client-Type", "extension")  # Default to extension for backward compatibility
        logger.info(f"[AUTH] Sign in for client_type: {client_type}")

        if client_type != "webapp" and client_type != "extension":
            logger.error(f"[AUTH] Unknown client_type: {client_type}")
            return HTTPException(status_code=400, detail="Unknown client type")

        response.set_cookie(
            key="session_token",
            value=session.access_token,
            httponly=True,
            secure=True,  # HTTPS only
            samesite="lax",
            max_age=7 * 24 * 60 * 60,  # 7 days
            path="/"
        )

        response.set_cookie(
            key="refresh_token",
            value=session.refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60,  # 7 days
            path="/"
        )
        

    except Exception as e:
        error_message = str(e)
        logger.error(f"Sign in error: {error_message}")

        # Check if it's an email not confirmed error
        if "Email not confirmed" in error_message or "email_not_confirmed" in error_message.lower():
            raise HTTPException(
                status_code=400,
                detail="Email not confirmed. Please check your email and click the confirmation link before signing in."
            )

        # Check if it's invalid credentials
        if "Invalid login credentials" in error_message or "invalid" in error_message.lower():
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Generic error for other cases
        raise HTTPException(status_code=500, detail=f"Unexpected error: {error_message}")
