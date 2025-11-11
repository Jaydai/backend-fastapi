from dataclasses import dataclass
from typing import List, Optional
from ..enums import RoleEnum, PermissionEnum


@dataclass
class UserOrganizationRole:
    """
    Association between a user and their role in a specific context
    Supports both global roles (organization_id=None) and organization-specific roles
    """
    user_id: str
    role: RoleEnum
    organization_id: Optional[str] = None  # None = global role, otherwise org-specific
    
    def has_permission(self, permission: PermissionEnum) -> bool:
        """
        Check if this role has a specific permission
        This follows the principle of Single Responsibility
        """
        return permission in ROLE_PERMISSIONS.get(self.role.name, [])
    
    def is_global(self) -> bool:
        """Check if this is a global role (not organization-specific)"""
        return self.organization_id is None
    
    def is_for_organization(self, organization_id: str) -> bool:
        """Check if this role is for a specific organization"""
        return self.organization_id == organization_id


# Role-Permission mapping following Open/Closed Principle
# Can be extended without modifying existing code
ROLE_PERMISSIONS: dict[RoleEnum, List[PermissionEnum]] = {
    RoleEnum.ADMIN: [
        # Admins have all permissions
        PermissionEnum.ADMIN_SETTINGS,

        PermissionEnum.COMMENT_CREATE,
        PermissionEnum.COMMENT_READ,
        PermissionEnum.COMMENT_UPDATE,
        PermissionEnum.COMMENT_DELETE,
        PermissionEnum.TEMPLATE_CREATE,
        PermissionEnum.TEMPLATE_READ,
        PermissionEnum.TEMPLATE_UPDATE,
        PermissionEnum.TEMPLATE_DELETE,
        PermissionEnum.BLOCK_CREATE,
        PermissionEnum.BLOCK_READ,
        PermissionEnum.BLOCK_UPDATE,
        PermissionEnum.BLOCK_DELETE,
        PermissionEnum.USER_CREATE,
        PermissionEnum.USER_READ,
        PermissionEnum.USER_UPDATE,
        PermissionEnum.USER_DELETE,
    ],
    RoleEnum.WRITER: [
        # Writers can manage content and read users
        PermissionEnum.COMMENT_CREATE,
        PermissionEnum.COMMENT_READ,
        PermissionEnum.COMMENT_UPDATE,
        PermissionEnum.COMMENT_DELETE,
        PermissionEnum.TEMPLATE_CREATE,
        PermissionEnum.TEMPLATE_READ,
        PermissionEnum.TEMPLATE_UPDATE,
        PermissionEnum.TEMPLATE_DELETE,
        PermissionEnum.BLOCK_CREATE,
        PermissionEnum.BLOCK_READ,
        PermissionEnum.BLOCK_UPDATE,
        PermissionEnum.BLOCK_DELETE,
    ],
    RoleEnum.VIEWER: [
        # Viewers can read and write their own content
        PermissionEnum.COMMENT_CREATE,
        PermissionEnum.COMMENT_READ,
        PermissionEnum.COMMENT_UPDATE,
        PermissionEnum.COMMENT_DELETE,
        PermissionEnum.TEMPLATE_READ,
        PermissionEnum.BLOCK_READ,
    ],
    RoleEnum.GUEST: [
        PermissionEnum.COMMENT_READ,
        PermissionEnum.TEMPLATE_READ,
        PermissionEnum.BLOCK_READ,
    ],
}
