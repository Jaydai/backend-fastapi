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
            raise HTTPException(status_code=400, detail="Unknown client type")

        # Set auth cookies
        set_auth_cookies(response, session)

        # Get Supabase auth user (for email, created_at, etc.)
        from core.supabase import supabase, create_authenticated_client
        auth_response = supabase.auth.get_user(session.access_token)
        auth_user = auth_response.user

        if not auth_user:
            raise HTTPException(status_code=500, detail="Failed to get user information")

        # Create authenticated client for this user (needed for RLS policies)
        client = create_authenticated_client(session.access_token)

        # Get user metadata (for name, profile_picture, etc.)
        try:
            metadata = AuthService.get_user_metadata(client, auth_user.id)
        except Exception as e:
            logger.warning(f"Could not get user metadata: {e}")
            # Create default metadata if it doesn't exist
            metadata = None

        # Return complete user info
        return {
            "success": True,
            "session": {
                "access_token": session.access_token,
                "refresh_token": session.refresh_token
            },
            "user": {
                "id": auth_user.id,
                "email": auth_user.email,
                "full_name": metadata.name if metadata else auth_user.user_metadata.get("full_name"),
                "avatar_url": metadata.profile_picture_url if metadata else auth_user.user_metadata.get("avatar_url"),
                "created_at": auth_user.created_at
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        error_message = str(e)
        logger.error(f"Sign in error: {error_message}")

        if "Invalid login credentials" in error_message or "invalid" in error_message.lower():
            raise HTTPException(status_code=401, detail="Invalid email or password")

        raise HTTPException(status_code=500, detail=f"Unexpected error: {error_message}")
