from core.supabase import supabase
from typing import Dict, Any

class AuthRepository:
    @staticmethod
    def sign_in_with_password(email: str, password: str) -> Dict[str, Any]:
        return supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
