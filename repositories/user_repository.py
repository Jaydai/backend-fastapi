from supabase import Client
from domains.entities import UserOrganizationRole

class UserRepository:
    @staticmethod
    def is_user_in_organization(client: Client, user_id: str, organization_id: str) -> bool:
        response = client.table("user_organization_roles") \
            .select("id") \
            .eq("user_id", user_id) \
            .eq("organization_id", organization_id) \
            .limit(1) \
            .execute()
        return bool(response.data)
    
    @staticmethod
    def create_user_organization_role(client: Client, user_id: str, organization_id: str, role: str) -> UserOrganizationRole | None:
        response = client.table("user_organization_roles") \
            .insert({
                "user_id": user_id,
                "organization_id": organization_id,
                "role": role
            }) \
            .execute()
        if not response.data:
            return None
        row = response.data[0]
        return UserOrganizationRole(
            id=row["id"],
            user_id=row["user_id"],
            organization_id=row["organization_id"],
            role=row["role"],
        )
