from dataclasses import dataclass
from typing import Optional

@dataclass
class Session:
    access_token: str
    refresh_token: str

@dataclass
class User:
    """User entity from Supabase auth"""
    user_id: Optional[str] = None
    name: Optional[str] = None
    data_collection: bool = True
    profile_picture_url: Optional[str] = None