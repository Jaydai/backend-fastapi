from domains.entities import Session
from core.supabase import supabase
from typing import Dict, Any

class AuthRepository:
    @staticmethod
    def sign_in_with_password(email: str, password: str) -> Session:
        sign_in_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        return Session(
            access_token=sign_in_response.session.access_token,
            refresh_token=sign_in_response.session.refresh_token
        )
