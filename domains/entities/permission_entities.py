from dataclasses import dataclass
from ..enums import RoleEnum, PermissionEnum


@dataclass
class UserOrganizationRole:
    user_id: str
    role: RoleEnum
    organization_id: str | None = None
    
    def has_permission(self, permission: PermissionEnum) -> bool:
        return permission in ROLE_PERMISSIONS.get(self.role.name, [])
    
    def is_global(self) -> bool:
        return self.organization_id is None
    
    def is_for_organization(self, organization_id: str) -> bool:
        return self.organization_id == organization_id

ROLE_PERMISSIONS: dict[RoleEnum, list[PermissionEnum]] = {
    RoleEnum.ADMIN: [
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
        PermissionEnum.ORGANIZATION_READ,
        PermissionEnum.ORGANIZATION_UPDATE,
    ],
    RoleEnum.WRITER: [
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
        PermissionEnum.ORGANIZATION_READ
    ],
    RoleEnum.VIEWER: [
        PermissionEnum.COMMENT_CREATE,
        PermissionEnum.COMMENT_READ,
        PermissionEnum.COMMENT_UPDATE,
        PermissionEnum.COMMENT_DELETE,
        PermissionEnum.TEMPLATE_READ,
        PermissionEnum.BLOCK_READ,
        PermissionEnum.ORGANIZATION_READ
    ],
    RoleEnum.GUEST: [
        PermissionEnum.COMMENT_READ,
        PermissionEnum.TEMPLATE_READ,
        PermissionEnum.BLOCK_READ,
        PermissionEnum.ORGANIZATION_READ
    ],
}
