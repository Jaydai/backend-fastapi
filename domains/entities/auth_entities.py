from dataclasses import dataclass


@dataclass
class Session:
    access_token: str
    refresh_token: str


@dataclass
class User:
    """User entity from users_metadata table.

    Note: Onboarding state is now stored in users_onboarding table
    and accessed via OnboardingRepository.
    """
    user_id: str | None = None
    name: str | None = None
    data_collection: bool = True
    profile_picture_url: str | None = None
    email: str | None = None
    created_at: str | None = None
