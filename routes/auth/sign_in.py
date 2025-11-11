"""Sign in endpoint"""
from fastapi import HTTPException, Request, Response
from . import router
from dtos import SignInDTO
import logging
from services import AuthService
from domains.entities import Session
from utils import set_auth_cookies

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

        set_auth_cookies(response, session)
        

    except Exception as e:
        error_message = str(e)
        logger.error(f"Sign in error: {error_message}")

        if "Invalid login credentials" in error_message or "invalid" in error_message.lower():
            raise HTTPException(status_code=401, detail="Invalid email or password")

        raise HTTPException(status_code=500, detail=f"Unexpected error: {error_message}")
