from domains.entities import UserOrganizationRole, UserProfile
from supabase import Client


class UserRepository:
    @staticmethod
    def is_user_in_organization(client: Client, user_id: str, organization_id: str) -> bool:
        response = (
            client.table("user_organization_roles")
            .select("id")
            .eq("user_id", user_id)
            .eq("organization_id", organization_id)
            .limit(1)
            .execute()
        )
        return bool(response.data)

    @staticmethod
    def create_user_organization_role(
        client: Client, user_id: str, organization_id: str, role: str
    ) -> UserOrganizationRole | None:
        response = (
            client.table("user_organization_roles")
            .insert({"user_id": user_id, "organization_id": organization_id, "role": role})
            .execute()
        )
        if not response.data:
            return None
        row = response.data[0]
        return UserOrganizationRole(
            id=row["id"],
            user_id=row["user_id"],
            organization_id=row["organization_id"],
            role=row["role"],
        )

    @staticmethod
    def get_user_profile(client: Client, user_id: str) -> UserProfile | None:
        try:
            response = (
                client.table("users_metadata")
                .select("name, phone_number, profile_picture_url, data_collection")
                .eq("user_id", user_id)
                .single()
                .execute()
            )

            if not response.data:
                return None

            metadata = response.data

            return UserProfile(
                id=user_id,
                email="",
                first_name=metadata.get("name"),
                last_name=None,
                avatar_url=metadata.get("profile_picture_url"),
                phone=metadata.get("phone_number"),
                created_at=None,
                email_confirmed_at=None,
            )
        except Exception:
            return None

    @staticmethod
    def update_user_profile(client: Client, user_id: str, update_data: dict) -> UserProfile | None:
        try:
            metadata_updates = {}

            if "first_name" in update_data:
                metadata_updates["name"] = update_data["first_name"]

            if "phone" in update_data:
                metadata_updates["phone_number"] = update_data["phone"]

            if "avatar_url" in update_data:
                metadata_updates["profile_picture_url"] = update_data["avatar_url"]

            if not metadata_updates:
                return UserRepository.get_user_profile(client, user_id)

            existing = client.table("users_metadata").select("id").eq("user_id", user_id).execute()

            if existing.data:
                client.table("users_metadata").update(metadata_updates).eq("user_id", user_id).execute()
            else:
                metadata_updates["user_id"] = user_id
                client.table("users_metadata").insert(metadata_updates).execute()

            return UserRepository.get_user_profile(client, user_id)
        except Exception:
            return None

    @staticmethod
    def update_data_collection(client: Client, user_id: str, data_collection: bool) -> bool:
        try:
            existing = client.table("users_metadata").select("id").eq("user_id", user_id).execute()

            if existing.data:
                client.table("users_metadata").update({"data_collection": data_collection}).eq(
                    "user_id", user_id
                ).execute()
            else:
                client.table("users_metadata").insert(
                    {"user_id": user_id, "data_collection": data_collection}
                ).execute()

            return True
        except Exception:
            return False
