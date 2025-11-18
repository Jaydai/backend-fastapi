from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request, status
from services import AuthService
from utils.auth_helpers import ACCESS_COOKIE_KEY
from core.supabase import SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY
from supabase import create_client, ClientOptions


class AuthenticationMiddleware(BaseHTTPMiddleware):
    PUBLIC_PATHS_WITHOUT_AUTH = [
        "/",
        "/docs", # TODO: désactiver en prod
        "/redoc",
        "/auth", # TODO: Rajouter de la ségrégation
    ]
    
    async def dispatch(self, request: Request, call_next):
        if self._is_public_route(request):
            return await call_next(request)
        
        try:
            access_token = request.cookies.get(ACCESS_COOKIE_KEY)
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
