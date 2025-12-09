import logging

from fastapi import HTTPException, Request, Response

from dtos import SignUpDTO
from services import AuthService
from utils import set_auth_cookies

from . import router

logger = logging.getLogger(__name__)


@router.post("/sign_up", status_code=201)
async def sign_up(sign_up_dto: SignUpDTO, request: Request, response: Response):
    try:
        session = AuthService.sign_up_with_email(sign_up_dto)

        client_type = request.headers.get(
            "X-Client-Type", "extension"
        )  # Default to extension for backward compatibility
        logger.info(f"[AUTH] Sign up for client_type: {client_type}")

        if client_type != "webapp" and client_type != "extension":
            logger.error(f"[AUTH] Unknown client_type: {client_type}")
            raise HTTPException(status_code=400, detail="Unknown client type")

        # If session is None, email confirmation is required
        if session is None:
            logger.info(f"[AUTH] Email confirmation required for: {sign_up_dto.email}")
            return {"message": "Email confirmation required", "email_confirmation_required": True}

        set_auth_cookies(response, session)
        return {"message": "Sign up successful", "email_confirmation_required": False}

    except Exception as e:
        error_message = str(e)
        logger.error(f"Sign up error: {error_message}")
        raise HTTPException(status_code=500, detail=f"Error during sign up: {error_message}")
