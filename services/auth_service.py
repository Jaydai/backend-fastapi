from dtos import SignInDTO, SignUpDTO, OAuthSignIn, RefreshTokenDTO
from repositories import AuthRepository
from domains.entities import Session


class AuthService:

    @staticmethod
    def sign_in_with_password(sign_in_dto: SignInDTO) -> Session:
        return AuthRepository.sign_in_with_password(sign_in_dto)
        
    @staticmethod
    def oauth_sign_in(sign_in_dto: OAuthSignIn) -> Session:
        return AuthRepository.oauth_sign_in(sign_in_dto)
    
    @staticmethod
    def sign_up_with_email(sign_up_dto: SignUpDTO) -> Session:
        return AuthRepository.sign_up_with_email(sign_up_dto)


    @staticmethod
    def sign_out(access_token: str | None) -> None:
        if access_token:
            AuthRepository.sign_out()

    @staticmethod
    def refresh_token(refresh_token_dto: RefreshTokenDTO) -> Session:
        return AuthRepository.refresh_session(refresh_token_dto)
    
    @staticmethod
    def get_current_user_id() -> str | None:
        return AuthRepository.get_current_user_id()
