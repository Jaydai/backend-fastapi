"""Me endpoint - get current authenticated user"""

import logging

from fastapi import HTTPException, Request, Response

from services import AuthService

from . import router

logger = logging.getLogger(__name__)


@router.get("/me")
async def get_me(request: Request, response: Response):
    """
    Get the current authenticated user with metadata.
    Supports both cookie-based (webapp) and bearer token (extension) auth.
    """
    try:
        try:
            user_id = request.state.user_id
        except AttributeError:
            raise HTTPException(status_code=401, detail="No authenticated user")

        if not user_id:
            logger.error("User not found")
            raise HTTPException(status_code=401, detail="No authenticated user")

        # Get authenticated Supabase client from middleware
        client = request.state.supabase_client
        user = AuthService.get_user_metadata(client, user_id)
        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"[USERS] Unexpected error in /users/me endpoint: {str(e)}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
