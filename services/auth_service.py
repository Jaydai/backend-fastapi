from dtos import SignInDTO
from typing import Dict, Any
from repositories import AuthRepository


class AuthService:

    @staticmethod
    def sign_in_with_password(sign_in_dto: SignInDTO) -> Dict[str, Any]:
        return AuthRepository.sign_in_with_password(
            email=sign_in_dto.email,
            password=sign_in_dto.password
        )
        
        