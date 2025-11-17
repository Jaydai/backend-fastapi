from collections.abc import Callable
from functools import wraps
from typing import Callable

from fastapi import HTTPException, Request, status

from fastapi import HTTPException, Request, status

from domains.enums import PermissionEnum
from services import PermissionService


def require_permission_in_organization(permission: PermissionEnum):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request: Request, *args, organization_id: str = None, **kwargs):
            user_id = request.state.user_id
            client = request.state.supabase_client

            # Extract organization_id from path params if needed
            if not organization_id:
                organization_id = kwargs.get("organization_id")

            if not organization_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Organization ID is required",
                )

            if not PermissionService.user_has_permission_in_organization(client, user_id, permission, organization_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied in organization {organization_id}. Required: {permission.value}",
                )

            request.state.organization_id = organization_id

            return await func(request, *args, organization_id=organization_id, **kwargs)

        return wrapper

    return decorator


def require_global_admin():
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            user_id = request.state.user_id
            client = request.state.supabase_client

            if not PermissionService.user_is_global_admin(client, user_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Global admin permission denied.",
                )

            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
