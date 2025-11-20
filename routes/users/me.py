"""Me endpoint - get current authenticated user"""
from fastapi import HTTPException, Response, Request
import logging

from . import router
from services import AuthService

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

        user = AuthService.get_user_metadata(user_id)
        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"[USERS] Unexpected error in /users/me endpoint: {str(e)}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

