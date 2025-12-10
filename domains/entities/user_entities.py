from dataclasses import dataclass


@dataclass
class User:
    user_id: str
    name: str | None = None
    data_collection: bool = True
    profile_picture_url: str | None = None
    email: str | None = None
    created_at: str | None = None
    onboarding_step: str | None = None
    onboarding_flow_type: str | None = None
    onboarding_completed_at: str | None = None


@dataclass
class UserProfile:
    id: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: str | None = None
    phone: str | None = None
    created_at: str | None = None
    email_confirmed_at: str | None = None
