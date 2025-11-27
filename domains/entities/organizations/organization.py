from dataclasses import dataclass
from typing import Literal

from ..permission_entities import UserOrganizationRole

OrganizationType = Literal["company", "standard"]


@dataclass
class Organization:
    id: str
    name: str
    user_organization_role: UserOrganizationRole | None = None  # None in case of a global Admin
    type: OrganizationType = "standard"  # "company" for legacy company workspaces
    image_url: str | None = None
    banner_url: str | None = None
    created_at: str | None = None
    website_url: str | None = None
