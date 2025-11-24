from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request, status
from services import AuthService
from utils.auth_helpers import ACCESS_COOKIE_KEY
from core.supabase import SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY
from supabase import create_client, ClientOptions
import logging

logger = logging.getLogger(__name__)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    PUBLIC_PATHS_WITHOUT_AUTH = [
        "/",
        "/enrichment",
        "/enrichment/enrich-message-batch",
        "/enrichment/enrich-chat-batch",
        "/docs", # TODO: désactiver en prod
        "/redoc",
        "/auth/sign_in",
        "/auth/sign_up",
        "/auth/sign_out",
        "/auth/oauth_sign_in",
        "/auth/refresh",
        "/auth/verify",
        "/auth/resend_verification",
        "/auth/reset_password",
        "/openapi.json",
    ]
    
    async def dispatch(self, request: Request, call_next):
        # Allow CORS preflight requests to pass through without authentication
        if request.method == "OPTIONS":
            return await call_next(request)

        if self._is_public_route(request):
            # For public routes, still provide an unauthenticated Supabase client
            from core.supabase import supabase
            request.state.supabase_client = supabase
            request.state.user_id = None
            return await call_next(request)

        try:
            # Try to get access_token from multiple sources:
            # 1. Authorization header (for extension and API clients)
            access_token = None
            auth_header = request.headers.get("authorization") or request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                access_token = auth_header[7:]  # Remove "Bearer " prefix

            # 2. Cookies (for webapp browser requests)
            if not access_token:
                access_token = request.cookies.get(ACCESS_COOKIE_KEY)

            # 3. Cookie header (for server-to-server requests)
            if not access_token:
                cookie_header = request.headers.get("cookie") or request.headers.get("Cookie", "")
                if cookie_header:
                    # Parse Cookie header: "access_token=xxx; refresh_token=yyy"
                    cookies_dict = {}
                    for cookie_pair in cookie_header.split(";"):
                        cookie_pair = cookie_pair.strip()
                        if "=" in cookie_pair:
                            key, value = cookie_pair.split("=", 1)
                            cookies_dict[key.strip()] = value.strip()
                    access_token = cookies_dict.get(ACCESS_COOKIE_KEY)

            if not access_token:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Missing access_token cookie."}
                )
            user_id = AuthService.get_current_user_id(access_token)
            if not user_id:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "detail": "Authentication required. Please provide a valid JWT token in cookies."
                    }
                )

            # Create an authenticated Supabase client for this request
            authenticated_client = create_client(
                SUPABASE_URL,
                SUPABASE_PUBLISHABLE_KEY,
                options=ClientOptions(
                    headers={
                        "Authorization": f"Bearer {access_token}"
                    }
                )
            )

            request.state.user_id = user_id
            request.state.supabase_client = authenticated_client
            
        except Exception:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Invalid authentication credentials. Token may be expired or malformed."
                }
            )
        
        response = await call_next(request)
        return response
    
    def _is_public_route(self, request: Request) -> bool:
        path = request.url.path
        
        if path in self.PUBLIC_PATHS_WITHOUT_AUTH:
            return True
        
        for public_path in self.PUBLIC_PATHS_WITHOUT_AUTH:
            if public_path != "/" and path.startswith(public_path):
                return True
        
        return False
