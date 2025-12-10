from dataclasses import dataclass


@dataclass
class Session:
    access_token: str
    refresh_token: str


@dataclass
class User:
    """User entity from Supabase auth"""
    user_id: str | None = None
    name: str | None = None
    data_collection: bool = True
    profile_picture_url: str | None = None
    email: str | None = None
    created_at: str | None = None
    onboarding_step: str | None = None
    onboarding_flow_type: str | None = None
    onboarding_completed_at: str | None = None
