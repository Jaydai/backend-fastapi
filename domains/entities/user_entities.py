from dataclasses import dataclass


# Note: User entity is defined in auth_entities.py


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
