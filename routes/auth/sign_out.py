from fastapi import Response, Request
from . import router
from services import AuthService
import logging

logger = logging.getLogger(__name__)


@router.post("/sign_out")
async def sign_out(request: Request, response: Response):
    try:
        client_type = request.headers.get("X-Client-Type", "extension")
        logger.info(f"[AUTH] Sign out for client_type: {client_type}")

        AuthService.sign_out(request.cookies.get("session_token"))

        response.delete_cookie(
            key="session_token",
            path="/"
        )
        response.delete_cookie(
            key="refresh_token",
            path="/"
        )

    except Exception as e:
        logger.error(f"Sign out error: {str(e)}")
