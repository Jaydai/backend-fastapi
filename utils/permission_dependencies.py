"""
Permission Dependencies
FastAPI dependencies for checking user permissions
Supports both global and organization-scoped permissions
Following Dependency Inversion Principle
"""
from typing import Callable, Optional
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer

from core.supabase import supabase
from services import PermissionService, AuthService
from domains.enums import PermissionEnum


# security = HTTPBearer()

# async def get_current_user_id(token: str = Depends(security)) -> str:
async def get_current_user_id() -> str:
    """
    Extract user_id from JWT token
    This dependency should be used as a base for other permission checks
    """
    try:
        # Verify the token with Supabase
        user_id = AuthService.get_current_user_id()

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        
        return user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


async def get_organization_id_from_header(
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-Id")
) -> Optional[str]:
    """
    Extract organization_id from header
    This is optional - if not provided, permissions are checked globally
    """
    return x_organization_id


def require_permission(permission: PermissionEnum, require_organization: bool = False) -> Callable:
    """
    Dependency factory that creates a permission checker
    
    Args:
        permission: The required permission
        require_organization: If True, organization_id header is mandatory
    
    Usage in routes:
        # Check permission globally:
        @router.get("/admin", dependencies=[Depends(require_permission(PermissionEnum.ADMIN_ACCESS))])
        
        # Check permission in organization context:
        @router.get("/org/content", dependencies=[Depends(require_permission(PermissionEnum.CONTENT_WRITE, require_organization=True))])
    
    This follows the Open/Closed Principle - you can add new permissions without modifying this code
    """
    async def permission_checker(
        user_id: str = Depends(get_current_user_id),
        organization_id: Optional[str] = Depends(get_organization_id_from_header)
    ) -> str:
        """Check if the current user has the required permission"""
        
        if require_organization and not organization_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization ID is required for this operation. Please provide X-Organization-Id header.",
            )
        
        if not PermissionService.user_has_permission(user_id, permission, organization_id):
            context = f" in organization {organization_id}" if organization_id else " globally"
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied{context}. Required permission: {permission.value}",
            )
        
        return user_id
    
    return permission_checker


def require_permission_in_organization(permission: PermissionEnum) -> Callable:
    """
    Shortcut for requiring permission in organization context
    Organization ID header is mandatory
    
    Usage:
        @router.get("/org/data", dependencies=[Depends(require_permission_in_organization(PermissionEnum.CONTENT_READ))])
    """
    return require_permission(permission, require_organization=True)


def require_role(role: str) -> Callable:
    """
    Dependency factory that requires a specific role
    Usage in routes:
        @router.get("/admin", dependencies=[Depends(require_role("admin"))])
    """
    async def role_checker(user_id: str = Depends(get_current_user_id)) -> str:
        """Check if the current user has the required role"""
        
        user_organization_role = PermissionService.get_user_organization_role(user_id)
        
        if not user_organization_role or user_organization_role.role.value != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {role}",
            )
        
        return user_id
    
    return role_checker


async def require_admin(user_id: str = Depends(get_current_user_id)) -> str:
    """
    Shortcut dependency for admin-only routes
    Usage:
        @router.get("/admin", dependencies=[Depends(require_admin)])
    """
    if not PermissionService.user_has_permission(user_id, PermissionEnum.ADMIN_ACCESS):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    
    return user_id


async def get_current_user_permissions(
    user_id: str = Depends(get_current_user_id),
    organization_id: Optional[str] = Depends(get_organization_id_from_header)
) -> list[PermissionEnum]:
    """
    Get all permissions for the current user in the given context
    Useful for frontend to show/hide UI elements
    """
    user_organization_roles = PermissionService.get_user_organization_roles(user_id, organization_id)
    
    if not user_organization_roles:
        return []
    
    # Collect all unique permissions from all roles
    all_permissions = set()
    for user_organization_role in user_organization_roles:
        role_permissions = PermissionService.get_role_permissions(user_organization_role.role)
        all_permissions.update(role_permissions.permissions)
    
    return list(all_permissions)
