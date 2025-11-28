import inspect
from collections.abc import Callable
from functools import wraps

from fastapi import HTTPException, Request, status

from domains.enums import PermissionEnum
from services import PermissionService


def require_permission_in_organization(permission: PermissionEnum):
    def decorator(func: Callable) -> Callable:
        # Check if the function accepts organization_id parameter
        sig = inspect.signature(func)
        accepts_org_id = "organization_id" in sig.parameters

        @wraps(func)
        async def wrapper(request: Request, *args, organization_id: str = None, **kwargs):
            user_id = request.state.user_id
            client = request.state.supabase_client

            # Try to get organization_id from multiple sources (in order of priority):
            # 1. X-Organization-Id header (set in middleware via request.state)
            # 2. Path parameter
            # 3. Keyword argument
            if not organization_id:
                organization_id = getattr(request.state, "organization_id", None)
            if not organization_id:
                organization_id = kwargs.get("organization_id")

            # If still no organization_id, it's optional - skip permission check
            # This allows the endpoint to work for personal templates without organization
            if organization_id:
                if not PermissionService.user_has_permission_in_organization(client, user_id, permission, organization_id):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Permission denied in organization {organization_id}. Required: {permission.value}",
                    )
                request.state.organization_id = organization_id

            # Only pass organization_id if the function accepts it
            if accepts_org_id:
                return await func(request, *args, organization_id=organization_id, **kwargs)
            else:
                return await func(request, *args, **kwargs)

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
