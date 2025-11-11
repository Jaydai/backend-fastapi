from dtos import SignInDTO, SignUpDTO
from repositories import AuthRepository
from domains.entities import Session


class AuthService:

    @staticmethod
    def sign_in_with_password(sign_in_dto: SignInDTO) -> Session:
        return AuthRepository.sign_in_with_password(sign_in_dto)
        
    @staticmethod
    def sign_up_with_email(sign_up_dto: SignUpDTO) -> Session:
        return AuthRepository.sign_up_with_email(sign_up_dto)
        