from fastapi import HTTPException, Request, Response
from . import router
from dtos import SignUpDTO
import logging
from services import AuthService

logger = logging.getLogger(__name__)


@router.post("/sign_up", status_code=201)
async def sign_up(sign_up_dto: SignUpDTO, request: Request, response: Response):
    try:
        session = AuthService.sign_up_with_email(sign_up_dto)

        client_type = request.headers.get("X-Client-Type", "extension")  # Default to extension for backward compatibility
        logger.info(f"[AUTH] Sign up for client_type: {client_type}")

        if client_type != "webapp" and client_type != "extension":
            logger.error(f"[AUTH] Unknown client_type: {client_type}")
            raise HTTPException(status_code=400, detail="Unknown client type")

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
        logger.error(f"Sign up error: {error_message}")
        raise HTTPException(status_code=500, detail=f"Error during sign up: {error_message}")
