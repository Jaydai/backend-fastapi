from domains.entities import Session
from dtos import SignInDTO, SignUpDTO, OAuthSignIn, RefreshTokenDTO
from core.supabase import supabase

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
        refresh_response = supabase.auth.refresh_session({
            "refresh_token": refresh_token_dto.refresh_token
        })
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
