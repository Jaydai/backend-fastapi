from dataclasses import dataclass
from typing import Optional

@dataclass
class Session:
    """Can be based on Supabase session object"""
    access_token: str
    refresh_token: str

@dataclass
class User:
    """User entity from Supabase auth"""
    user_id: str
    name: str
    data_collection: bool
    profile_picture_url: Optional[str]