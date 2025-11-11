from fastapi import HTTPException, Request, Response
from . import router
from dtos import RefreshTokenDTO
import logging
from services import AuthService
from domains.entities import Session
from utils import set_auth_cookies

logger = logging.getLogger(__name__)


@router.post("/refresh")
async def refresh_token(request: Request, response: Response):
    try:
        refresh_token = request.cookies.get("refresh_token")
        
        if not refresh_token:
            logger.error("[AUTH] No refresh token found in cookies")
            raise HTTPException(status_code=401, detail="No refresh token provided")

        refresh_token_dto = RefreshTokenDTO(refresh_token=refresh_token)
        
        session: Session = AuthService.refresh_token(refresh_token_dto)

        client_type = request.headers.get("X-Client-Type", "extension")
        logger.info(f"[AUTH] Refresh token for client_type: {client_type}")

        if client_type not in ["webapp", "extension"]:
            logger.error(f"[AUTH] Unknown client_type: {client_type}")
            raise HTTPException(status_code=400, detail="Unknown client type")

        set_auth_cookies(response, session)

        logger.info("[AUTH] Token refreshed successfully")
        
    except Exception as e:
        error_message = str(e)
        logger.error(f"[AUTH] Refresh token error: {error_message}")

        if "invalid" in error_message.lower() or "expired" in error_message.lower():
            raise HTTPException(
                status_code=401, 
                detail="Invalid or expired refresh token. Please sign in again."
            )

        raise HTTPException(
            status_code=500, 
            detail=f"Unexpected error during token refresh: {error_message}"
        )
