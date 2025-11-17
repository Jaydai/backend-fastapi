import logging

from fastapi import Request, Response

from services import AuthService
from utils import clear_auth_cookies

from . import router

logger = logging.getLogger(__name__)


@router.post("/sign_out")
async def sign_out(request: Request, response: Response):
    try:
        client_type = request.headers.get("X-Client-Type", "extension")
        logger.info(f"[AUTH] Sign out for client_type: {client_type}")

        AuthService.sign_out(request.cookies.get("session_token"))

        clear_auth_cookies(response)

    except Exception as e:
        logger.error(f"Sign out error: {str(e)}")
