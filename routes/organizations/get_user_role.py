"""Get user's role in organization"""

import logging

from fastapi import HTTPException, Request

from domains.enums import RoleEnum
from repositories.permission_repository import PermissionRepository

from . import router

logger = logging.getLogger(__name__)


@router.get("/{organization_id}/user-role")
async def get_user_role_in_organization(request: Request, organization_id: str):
    """Get current user's role in the specified organization"""
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        # Get user's roles in this organization
        roles = PermissionRepository.get_user_organization_roles(client, user_id, organization_id)

        if not roles:
            return {"role": None, "has_role": False}

        # Get the highest priority role for this organization
        # Priority: admin > writer > viewer > guest
        role_priority = {RoleEnum.ADMIN: 4, RoleEnum.WRITER: 3, RoleEnum.VIEWER: 2, RoleEnum.GUEST: 1}

        # Filter to only organization-specific roles (not global)
        org_roles = [r for r in roles if r.organization_id == organization_id]

        if not org_roles:
            # Check if user has global admin role
            global_roles = [r for r in roles if r.is_global()]
            if any(r.role == RoleEnum.ADMIN for r in global_roles):
                return {"role": "admin", "has_role": True, "is_global_admin": True}
            return {"role": None, "has_role": False}

        # Get the highest priority role
        highest_role = max(org_roles, key=lambda r: role_priority.get(r.role, 0))

        return {"role": highest_role.role.value, "has_role": True, "is_global_admin": False}

    except Exception as e:
        logger.error(f"Error getting user role for organization {organization_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get user role: {str(e)}")
