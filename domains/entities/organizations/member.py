from dataclasses import dataclass


@dataclass
class OrganizationMember:
    user_id: str
    email: str
    role: str
    first_name: str | None = None
    last_name: str | None = None
