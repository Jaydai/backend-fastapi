from functools import wraps
from typing import Callable

from fastapi import HTTPException, Request, status

from services import PermissionService
from domains.enums import PermissionEnum


def require_permission_in_organization(permission: PermissionEnum):
    """Decorator to enforce that the caller has a given organization-scoped permission."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request: Request, *args, organization_id: str = None, **kwargs):
            user_id = request.state.user_id

            # Extract organization_id from path params if needed
            if not organization_id:
                organization_id = kwargs.get("organization_id")

            if not organization_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Organization ID is required",
                )

            if not PermissionService.user_has_permission_in_organization(user_id, permission, organization_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied in organization {organization_id}. Required: {permission.value}",
                )

            request.state.organization_id = organization_id

            return await func(request, *args, organization_id=organization_id, **kwargs)

        return wrapper

    return decorator


def require_global_admin():
    """Decorator for global admin-only routes."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            user_id = request.state.user_id

            if not PermissionService.user_is_global_admin(user_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Global admin permission denied.",
                )

            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
