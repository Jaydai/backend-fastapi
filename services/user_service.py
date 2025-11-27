from supabase import Client

from domains.entities import UserOrganizationRole
from dtos import UpdateUserProfileDTO, UserProfileResponseDTO
from repositories import UserRepository


class UserService:
    @staticmethod
    def get_email_by_id(client: Client, user_id: str) -> str:
        # Get email from users_metadata table instead of auth API
        response = client.table("users_metadata").select("email").eq("user_id", user_id).single().execute()
        if response.data and response.data.get("email"):
            return response.data["email"]
        raise ValueError("User email not found")

    @staticmethod
    def is_member_of_organization(client: Client, user_id: str, organization_id: str) -> bool:
        return UserRepository.is_user_in_organization(client, user_id, organization_id)

    @staticmethod
    def create_user_organization_role(
        client: Client, user_id: str, organization_id: str, role: str
    ) -> UserOrganizationRole:
        if UserService.is_member_of_organization(client, user_id, organization_id):
            raise ValueError("User is already a member of the organization")
        user_organization_role = UserRepository.create_user_organization_role(client, user_id, organization_id, role)
        if not user_organization_role:
            raise ValueError("Failed to create user organization role")
        return user_organization_role

    @staticmethod
    def get_user_profile(client: Client, user_id: str) -> UserProfileResponseDTO:
        profile = UserRepository.get_user_profile(client, user_id)

        if not profile:
            raise ValueError(f"User profile not found for user_id: {user_id}")

        return UserProfileResponseDTO(
            id=profile.id,
            email=profile.email,
            first_name=profile.first_name,
            last_name=profile.last_name,
            avatar_url=profile.avatar_url,
            phone=profile.phone,
            created_at=profile.created_at,
            email_confirmed_at=profile.email_confirmed_at,
        )

    @staticmethod
    def update_user_profile(client: Client, user_id: str, update_data: UpdateUserProfileDTO) -> UserProfileResponseDTO:
        # Convert DTO to dict, excluding None values
        update_dict = {}
        if update_data.first_name is not None:
            update_dict["first_name"] = update_data.first_name
        if update_data.last_name is not None:
            update_dict["last_name"] = update_data.last_name
        if update_data.phone is not None:
            update_dict["phone"] = update_data.phone

        if not update_dict:
            # No changes to make, just return current profile
            return UserService.get_user_profile(client, user_id)

        # Update profile
        updated_profile = UserRepository.update_user_profile(client, user_id, update_dict)

        if not updated_profile:
            raise ValueError("Failed to update user profile")

        return UserProfileResponseDTO(
            id=updated_profile.id,
            email=updated_profile.email,
            first_name=updated_profile.first_name,
            last_name=updated_profile.last_name,
            avatar_url=updated_profile.avatar_url,
            phone=updated_profile.phone,
            created_at=updated_profile.created_at,
            email_confirmed_at=updated_profile.email_confirmed_at,
        )

    @staticmethod
    def update_data_collection(client: Client, user_id: str, data_collection: bool) -> None:
        success = UserRepository.update_data_collection(client, user_id, data_collection)

        if not success:
            raise ValueError("Failed to update data collection preference")
