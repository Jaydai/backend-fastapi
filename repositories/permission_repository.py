from supabase import Client
from domains.entities import UserOrganizationRole
from domains.enums import RoleEnum


class PermissionRepository:
    @staticmethod
    def get_user_organization_roles(client: Client, user_id: str, organization_id: str) -> list[UserOrganizationRole]:
        try:
            query = client.table("user_organization_roles").select("*").eq("user_id", user_id)
            query = query.or_(f"organization_id.eq.{organization_id},organization_id.is.null")
            response = query.execute()

            if not response.data:
                return []

            return [
                UserOrganizationRole(
                    user_id=row["user_id"],
                    role=RoleEnum(row["role"]),
                    organization_id=row.get("organization_id")
                )
                for row in response.data
            ]
        except Exception as e:
            return []

    @staticmethod
    def get_user_global_roles(client: Client, user_id: str) -> list[UserOrganizationRole]:
        try:
            query = client.table("user_organization_roles").select("*").eq("user_id", user_id)
            query = query.is_("organization_id", "null")
            response = query.execute()

            if not response.data:
                return []

            return [
                UserOrganizationRole(
                    user_id=row["user_id"],
                    role=RoleEnum(row["role"]),
                    organization_id=row.get("organization_id")
                )
                for row in response.data
            ]
        except Exception as e:
            return []

    @staticmethod
    def get_user_all_roles(client: Client, user_id: str) -> list[UserOrganizationRole]:
        """
        Return ALL (global + organizations)
        """
        try:
            query = client.table("user_organization_roles").select("*").eq("user_id", user_id)
            response = query.execute()

            if not response.data:
                return []

            return [
                UserOrganizationRole(
                    user_id=row["user_id"],
                    role=RoleEnum(row["role"]),
                    organization_id=row.get("organization_id")
                )
                for row in response.data
            ]
        except Exception as e:
            return []
