from repositories import PermissionRepository
from domains.entities import UserOrganizationRole
from domains.enums import RoleEnum, PermissionEnum


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
    def user_has_permission_in_organization(user_id: str, permission: PermissionEnum, organization_id: str) -> bool:
        if PermissionService._is_global_resource(organization_id):
            return True
        
        roles: list[UserOrganizationRole] = PermissionRepository.get_user_organization_roles(user_id, organization_id)
        if not roles:
            return False
        
        global_roles = [r for r in roles if r.is_global()]
        org_roles = [r for r in roles if r.is_for_organization(organization_id)]
        
        return PermissionService._check_organization_permission(org_roles, global_roles, permission)

    @staticmethod
    def user_is_global_admin(user_id: str) -> bool:
        global_roles = PermissionRepository.get_user_global_roles(user_id)
        return PermissionService._is_global_admin(global_roles)