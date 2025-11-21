from domains.entities import Session, User
from dtos import SignInDTO, SignUpDTO, OAuthSignIn, RefreshTokenDTO
from core.supabase import supabase
from supabase import Client

class AuthRepository:
    @staticmethod
    def sign_in_with_password(sign_in_dto: SignInDTO) -> Session:
        sign_in_response = supabase.auth.sign_in_with_password({
            "email": sign_in_dto.email,
            "password": sign_in_dto.password,
        })
        return Session(
            access_token=sign_in_response.session.access_token,
            refresh_token=sign_in_response.session.refresh_token
        )
    
    @staticmethod
    def oauth_sign_in(sign_in_dto: OAuthSignIn) -> Session:
        sign_in_response = supabase.auth.sign_in_with_id_token({
            "provider": sign_in_dto.provider,
            "token": sign_in_dto.token
        })
        return Session(
            access_token=sign_in_response.session.access_token,
            refresh_token=sign_in_response.session.refresh_token
        )

    @staticmethod
    def sign_up_with_email(sign_up_dto: SignUpDTO) -> Session:
        # TODO: sign_up with email validation
        sign_up_response = supabase.auth.sign_up({
            "email": sign_up_dto.email,
            "password": sign_up_dto.password,
            "options": {
                "data": {
                    "first_name": sign_up_dto.first_name,
                    "last_name": sign_up_dto.last_name
                }
            }
        })
        return Session(
            access_token=sign_up_response.session.access_token,
            refresh_token=sign_up_response.session.refresh_token
        )

    @staticmethod
    def sign_out() -> None:
        supabase.auth.sign_out()

    @staticmethod
    def refresh_session(refresh_token_dto: RefreshTokenDTO) -> Session:
        refresh_response = supabase.auth.refresh_session(
            refresh_token_dto.refresh_token
        )
        return Session(
            access_token=refresh_response.session.access_token,
            refresh_token=refresh_response.session.refresh_token
        )

    @staticmethod
    def get_current_user_id(jwt: str) -> str | None:
        response = supabase.auth.get_user(jwt)
        if response.user:
            return response.user.id
        return None


 
    @staticmethod
    def get_user_metadata(client: Client, user_id: str) -> User:
        """Get user metadata from users_metadata table"""
        response = (
            client.table("users_metadata")
            .select("user_id, name, data_collection, profile_picture_url")
            .eq("user_id", user_id)
            .execute()
        )

        # If user metadata doesn't exist, create it
        if not response.data or len(response.data) == 0:
            # Create default user metadata
            new_user_data = {
                "user_id": user_id,
                "name": None,
                "data_collection": True,  # Default to True
                "profile_picture_url": None
            }

            insert_response = (
                client.table("users_metadata")
                .insert(new_user_data)
                .execute()
            )

            if insert_response.data and len(insert_response.data) > 0:
                return User(**insert_response.data[0])

            # If insert failed, return default User
            return User(user_id=user_id, name=None, data_collection=True, profile_picture_url=None)

        return User(**response.data[0])

