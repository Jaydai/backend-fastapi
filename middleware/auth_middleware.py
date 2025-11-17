from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request, status
from services import AuthService


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
            user_id = AuthService.get_current_user_id()
            
            if not user_id:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "detail": "Authentication required. Please provide a valid JWT token."
                    }
                )
            
            request.state.user_id = user_id
            
        except Exception as e:
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
            if path.startswith(public_path):
                return True
        
        return False
