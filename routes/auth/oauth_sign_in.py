from fastapi import HTTPException, Request, Response
from pydantic import BaseModel
from . import router, supabase
from dtos import OAuthSignIn
from services import AuthService
from utils import set_auth_cookies
import logging

logger = logging.getLogger(__name__)

@router.post("/oauth_sign_in")
async def oauth_sign_in(auth_request: OAuthSignIn, request: Request, response: Response):
    try:
        session = AuthService.oauth_sign_in(auth_request)
        
        
        client_type = request.headers.get("X-Client-Type", "extension")  # Default to extension for backward compatibility
        logger.info(f"[AUTH] Sign in for client_type: {client_type}")

        if client_type != "webapp" and client_type != "extension":
            logger.error(f"[AUTH] Unknown client_type: {client_type}")
            return HTTPException(status_code=400, detail="Unknown client type")

        set_auth_cookies(response, session)
        

    except Exception as e:
        error_message = str(e)
        logger.error(f"Sign in error: {error_message}")

        if "Email not confirmed" in error_message or "email_not_confirmed" in error_message.lower():
            raise HTTPException(
                status_code=400,
                detail="Email not confirmed. Please check your email and click the confirmation link before signing in."
            )

        if "Invalid login credentials" in error_message or "invalid" in error_message.lower():
            raise HTTPException(status_code=401, detail="Invalid email or password")

        raise HTTPException(status_code=500, detail=f"Unexpected error: {error_message}")

