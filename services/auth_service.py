from supabase import Client

from domains.entities import Session, User
from dtos import OAuthSignIn, RefreshTokenDTO, SignInDTO, SignUpDTO
from repositories import AuthRepository


class AuthService:
    @staticmethod
    def sign_in_with_password(sign_in_dto: SignInDTO) -> Session:
        return AuthRepository.sign_in_with_password(sign_in_dto)

    @staticmethod
    def oauth_sign_in(sign_in_dto: OAuthSignIn) -> Session:
        return AuthRepository.oauth_sign_in(sign_in_dto)

    @staticmethod
    def sign_up_with_email(sign_up_dto: SignUpDTO) -> Session | None:
        return AuthRepository.sign_up_with_email(sign_up_dto)

    @staticmethod
    def sign_out(access_token: str | None) -> None:
        if access_token:
            AuthRepository.sign_out()

    @staticmethod
    def refresh_token(refresh_token_dto: RefreshTokenDTO) -> Session:
        return AuthRepository.refresh_session(refresh_token_dto)

    @staticmethod
    def get_current_user_id(access_token: str) -> str | None:
        return AuthRepository.get_current_user_id(access_token)

    @staticmethod
    def get_user_metadata(client: Client, user_id: str) -> User:
        return AuthRepository.get_user_metadata(client, user_id)
