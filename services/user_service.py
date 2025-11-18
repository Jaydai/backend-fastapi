from supabase import Client
from repositories import UserRepository
from domains.entities import UserOrganizationRole

class UserService:
    @staticmethod
    def get_email_by_id(client: Client, user_id: str) -> str:
        user_response = client.auth.get_user(user_id)
        if user_response and user_response.user:
            return user_response.user.email
        raise ValueError("User email not found")
        
    @staticmethod
    def is_member_of_organization(client: Client, user_id: str, organization_id: str) -> bool:
        return UserRepository.is_user_in_organization(client, user_id, organization_id)
    
    @staticmethod
    def create_user_organization_role(client: Client, user_id: str, organization_id: str, role: str) -> UserOrganizationRole:
        if UserService.is_member_of_organization(client, user_id, organization_id):
            raise ValueError("User is already a member of the organization")
        user_organization_role = UserRepository.create_user_organization_role(client, user_id, organization_id, role)
        if not user_organization_role:
            raise ValueError("Failed to create user organization role")
        return user_organization_role