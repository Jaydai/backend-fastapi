from supabase import Client
from repositories import PermissionRepository
from domains.entities import UserOrganizationRole
from domains.enums import PermissionEnum, RoleEnum
from repositories import PermissionRepository


class PermissionService:
    @staticmethod
    def _is_global_resource(organization_id: str | None) -> bool:
        return organization_id is None

    @staticmethod
    def _check_organization_permission(
        org_roles: list[UserOrganizationRole],
        global_roles: list[UserOrganizationRole],
        permission: PermissionEnum
    ) -> bool:
        for role in org_roles:
            if role.has_permission(permission):
                return True
        for role in global_roles:
            if role.role == RoleEnum.ADMIN:
                return True
        return False

    @staticmethod
    def _is_global_admin(
        global_roles: list[UserOrganizationRole],
    ) -> bool:
        for role in global_roles:
            if role.role == RoleEnum.ADMIN:
                return True
        return False

    @staticmethod
    def user_has_permission(client: Client, user_id: str, permission: PermissionEnum, organization_id: str | None = None) -> bool:
        """Check if user has permission for a resource (organization or global)."""
        if PermissionService._is_global_resource(organization_id):
            # Global resources are PUBLIC - accessible to everyone
            # Only READ permissions are allowed for global resources without a global admin role
            if permission in [PermissionEnum.TEMPLATE_READ, PermissionEnum.BLOCK_READ]:
                return True

            # For write operations on global resources, require global admin
            global_roles = PermissionRepository.get_user_global_roles(client, user_id)
            return PermissionService._is_global_admin(global_roles)

        # Organization-specific resource
        roles: list[UserOrganizationRole] = PermissionRepository.get_user_organization_roles(client, user_id, organization_id)
        if not roles:
            return False

        global_roles = [r for r in roles if r.is_global()]
        org_roles = [r for r in roles if r.is_for_organization(organization_id)]

        return PermissionService._check_organization_permission(org_roles, global_roles, permission)

    @staticmethod
    def user_has_permission_in_organization(client: Client, user_id: str, permission: PermissionEnum, organization_id: str) -> bool:
        """Alias for user_has_permission for backward compatibility."""
        return PermissionService.user_has_permission(client, user_id, permission, organization_id)

    @staticmethod
    def user_is_global_admin(client: Client, user_id: str) -> bool:
        global_roles = PermissionRepository.get_user_global_roles(client, user_id)
        return PermissionService._is_global_admin(global_roles)
