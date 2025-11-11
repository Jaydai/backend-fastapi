from dataclasses import dataclass

@dataclass
class Session:
    """Can be based on Supabase session object"""
    access_token: str
    refresh_token: str
