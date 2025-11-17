from dataclasses import dataclass


@dataclass
class User:
    id: str


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
