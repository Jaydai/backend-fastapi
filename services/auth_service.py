from dtos import SignInDTO
from repositories import AuthRepository
from domains.entities import Session


class AuthService:

    @staticmethod
    def sign_in_with_password(sign_in_dto: SignInDTO) -> Session:
        return AuthRepository.sign_in_with_password(
            email=sign_in_dto.email,
            password=sign_in_dto.password
        )
        
        