from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from services.locale_service import LocaleService


class LocaleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        locale = LocaleService.extract_locale_from_request(request)
        request.state.locale = locale
        return await call_next(request)
