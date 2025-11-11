"""
Permission Repository
Handles data access for permissions and roles
Following the Repository Pattern and Dependency Inversion Principle
"""
from typing import Optional, List

from core.supabase import supabase
from domains.entities import UserOrganizationRole
from domains.enums import RoleEnum
from dtos import AssignRoleDTO, RemoveRoleDTO


class PermissionRepository:
    """Repository for permission-related database operations - Data access only"""

    @staticmethod
    def get_user_organization_roles(user_id: str, organization_id: Optional[str] = None) -> List[UserOrganizationRole]:
        """
        Get all roles assigned to a user from the database
        Returns UserOrganizationRole entities
        If organization_id is provided, returns roles for that organization + global roles
        If organization_id is None, returns only global roles
        """
        try:
            query = supabase.table("user_organization_roles").select("*").eq("user_id", user_id)
            
            if organization_id:
                # Get roles for this specific organization OR global roles
                query = query.or_(f"organization_id.eq.{organization_id},organization_id.is.null")
            else:
                # Get only global roles
                query = query.is_("organization_id", "null")
            
            response = query.execute()
            
            if not response.data:
                return []
            
            # Transform raw data into UserOrganizationRole entities
            return [
                UserOrganizationRole(
                    user_id=row["user_id"],
                    role=RoleEnum(row["role_name"]),
                    organization_id=row.get("organization_id")
                )
                for row in response.data
            ]
        except Exception as e:
            return []

    @staticmethod
    def assign_role(assign_role_dto: AssignRoleDTO) -> UserOrganizationRole:
        """
        Assign a role to a user in the database
        Creates or updates the user_organization_role record for the specified organization context
        Returns UserOrganizationRole entity
        """
        role_data = {
            "user_id": assign_role_dto.user_id,
            "role_name": assign_role_dto.role.value,
            "organization_id": assign_role_dto.organization_id,
        }
        
        # Check if user already has a role in this context
        query = supabase.table("user_organization_roles").select("*").eq("user_id", assign_role_dto.user_id)
        
        if assign_role_dto.organization_id:
            query = query.eq("organization_id", assign_role_dto.organization_id)
        else:
            query = query.is_("organization_id", "null")
        
        existing = query.execute()
        
        if existing.data:
            # Update existing role
            update_query = supabase.table("user_organization_roles").update(role_data).eq("user_id", assign_role_dto.user_id)
            if assign_role_dto.organization_id:
                update_query = update_query.eq("organization_id", assign_role_dto.organization_id)
            else:
                update_query = update_query.is_("organization_id", "null")
            response = update_query.execute()
        else:
            # Insert new role
            response = supabase.table("user_organization_roles").insert(role_data).execute()
        
        if not response.data:
            raise Exception("Failed to assign role")
        
        # Transform raw data into UserOrganizationRole entity
        row = response.data[0]
        return UserOrganizationRole(
            user_id=row["user_id"],
            role=RoleEnum(row["role_name"]),
            organization_id=row.get("organization_id")
        )

    @staticmethod
    def remove_role(remove_role_dto: RemoveRoleDTO) -> bool:
        """
        Remove a role from a user in a specific context
        Returns True if successful, False otherwise
        """
        try:
            query = supabase.table("user_organization_roles").delete().eq("user_id", remove_role_dto.user_id)
            
            if remove_role_dto.organization_id:
                query = query.eq("organization_id", remove_role_dto.organization_id)
            else:
                query = query.is_("organization_id", "null")
            
            query.execute()
            return True
        except Exception:
            return False
