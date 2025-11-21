from dataclasses import dataclass
from typing import Literal
from .member import OrganizationMember


OrganizationType = Literal["company", "standard"]


@dataclass
class OrganizationDetail:
    id: str
    name: str
    description: dict | None = None
    type: OrganizationType = "standard"
    image_url: str | None = None
    banner_url: str | None = None
    website_url: str | None = None
    created_at: str | None = None
    user_role: str | None = None  # Current user's role
    members: list[OrganizationMember] = None

    def __post_init__(self):
        if self.members is None:
            self.members = []
