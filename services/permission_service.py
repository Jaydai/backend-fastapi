"""
Permission Service
Business logic for permission and role management
Following Single Responsibility and Dependency Inversion Principles
"""
from typing import List, Optional

from repositories import PermissionRepository
from domains.entities import UserOrganizationRole, ROLE_PERMISSIONS
from domains.enums import RoleEnum, PermissionEnum
from dtos import (
    AssignRoleDTO,
    RemoveRoleDTO,
    CheckPermissionDTO,
    UserRoleResponseDTO,
    RolePermissionsResponseDTO,
)


class PermissionService:
    """Service layer for permission-related operations - Business logic only"""

    @staticmethod
    def _prioritize_roles(roles: List[UserOrganizationRole], organization_id: Optional[str]) -> Optional[UserOrganizationRole]:
        """
        Business logic: Prioritize organization-specific roles over global ones
        Returns the most relevant role for the given context
        """
        if not roles:
            return None
        
        # Prioritize organization-specific roles over global ones
        if organization_id:
            org_specific = [r for r in roles if r.organization_id == organization_id]
            if org_specific:
                return org_specific[0]
        
        # Return global role if exists
        global_roles = [r for r in roles if r.organization_id is None]
        return global_roles[0] if global_roles else roles[0]

    @staticmethod
    def get_user_organization_roles(user_id: str, organization_id: Optional[str] = None) -> List[UserRoleResponseDTO]:
        """
        Get all roles assigned to a user
        If organization_id is provided, returns roles for that organization + global roles
        Business logic: Convert entities to DTOs
        """
        user_organization_roles = PermissionRepository.get_user_organization_roles(user_id, organization_id)
        
        # Convert to DTOs for API response
        return [
            UserRoleResponseDTO(
                user_id=ur.user_id,
                role=ur.role.value,
                organization_id=ur.organization_id,
            )
            for ur in user_organization_roles
        ]

    @staticmethod
    def get_user_organization_role(user_id: str, organization_id: Optional[str] = None) -> Optional[UserRoleResponseDTO]:
        """
        Get the role assigned to a user in a specific context
        Business logic: Prioritizes organization-specific over global roles
        Returns None if no role is assigned
        """
        user_organization_roles = PermissionRepository.get_user_organization_roles(user_id, organization_id)
        
        # Apply business logic: prioritize roles
        prioritized_role = PermissionService._prioritize_roles(user_organization_roles, organization_id)
        
        if not prioritized_role:
            return None
        
        return UserRoleResponseDTO(
            user_id=prioritized_role.user_id,
            role=prioritized_role.role.value,
            organization_id=prioritized_role.organization_id,
        )

    @staticmethod
    def assign_role(assign_role_dto: AssignRoleDTO) -> UserRoleResponseDTO:
        """
        Assign a role to a user in a specific context (organization or global)
        Business logic: Convert entity to DTO
        Only users with ROLE_ASSIGN permission can do this
        """
        user_organization_role = PermissionRepository.assign_role(assign_role_dto)
        
        return UserRoleResponseDTO(
            user_id=user_organization_role.user_id,
            role=user_organization_role.role.value,
            organization_id=user_organization_role.organization_id,
        )

    @staticmethod
    def remove_role(remove_role_dto: RemoveRoleDTO) -> bool:
        """
        Remove a role from a user in a specific context
        Only users with ROLE_REMOVE permission can do this
        """
        return PermissionRepository.remove_role(remove_role_dto)

    @staticmethod
    def check_permission(check_permission_dto: CheckPermissionDTO) -> bool:
        """
        Check if a user has a specific permission in a given context
        Business logic: Get user roles and check permissions
        """
        user_organization_roles = PermissionRepository.get_user_organization_roles(
            check_permission_dto.user_id,
            check_permission_dto.organization_id
        )
        
        if not user_organization_roles:
            return False
        
        # Business logic: Check if any of the user's roles has this permission
        for user_organization_role in user_organization_roles:
            if user_organization_role.has_permission(check_permission_dto.permission):
                return True
        
        return False

    @staticmethod
    def get_role_permissions(role: RoleEnum) -> RolePermissionsResponseDTO:
        """
        Get all permissions for a specific role
        Business logic: Access ROLE_PERMISSIONS mapping
        """
        permissions = ROLE_PERMISSIONS.get(role, [])
        
        return RolePermissionsResponseDTO(
            role=role,
            permissions=permissions,
            description=f"Permissions for {role.value} role"
        )

    @staticmethod
    def get_all_roles_with_permissions() -> List[RolePermissionsResponseDTO]:
        """
        Get all roles with their respective permissions
        Business logic: Iterate through all roles and get their permissions
        Useful for admin interfaces
        """
        result = []
        for role in RoleEnum:
            permissions = ROLE_PERMISSIONS.get(role, [])
            result.append(
                RolePermissionsResponseDTO(
                    role=role,
                    permissions=permissions,
                    description=f"Permissions for {role.value} role"
                )
            )
        return result

    @staticmethod
    def user_has_permission(user_id: str, permission: PermissionEnum, organization_id: Optional[str] = None) -> bool:
        """
        Check if a user has a specific permission based on their role
        This is the main method used by route dependencies
        Business logic: Get roles and check permissions
        Checks in the context of an organization if provided
        """
        user_organization_roles = PermissionRepository.get_user_organization_roles(user_id, organization_id)
        
        if not user_organization_roles:
            return False
        
        # Business logic: Check if any of the user's roles has this permission
        for user_organization_role in user_organization_roles:
            if user_organization_role.has_permission(permission):
                return True
        
        return False

    @staticmethod
    def user_can_access_resource_in_organization(
        user_id: str, 
        permission: PermissionEnum, 
        resource_organization_id: Optional[str],
        requested_organization_id: Optional[str] = None
    ) -> bool:
        """
        Check if a user can access a resource with a specific permission in an organization context
        
        Business logic:
        - If resource is global (resource_organization_id=None), user must have global permission
        - If resource belongs to an organization, user must have permission in THAT organization
        - Prevents cross-organization access
        
        Args:
            user_id: The user ID
            permission: The required permission
            resource_organization_id: The organization that owns the resource (None = global)
            requested_organization_id: The organization context from the request (optional)
        
        Returns:
            True if user can access the resource, False otherwise
        """
        if resource_organization_id and requested_organization_id:
            if resource_organization_id != requested_organization_id:
                return False
        
        user_organization_roles = PermissionRepository.get_user_organization_roles(
            user_id, 
            resource_organization_id
        )
        
        if not user_organization_roles:
            return False
        
        # Check if any role has the required permission
        for user_organization_role in user_organization_roles:
            # Only count roles that match the organization context
            if resource_organization_id:
                # Resource is organization-specific: user needs role in that org
                if user_organization_role.organization_id == resource_organization_id:
                    if user_organization_role.has_permission(permission):
                        return True
            else:
                # Resource is global: user needs global role
                if user_organization_role.is_global():
                    if user_organization_role.has_permission(permission):
                        return True
        
        return False
