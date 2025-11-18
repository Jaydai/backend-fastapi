from dataclasses import dataclass
from ..permission_entities import UserOrganizationRole


@dataclass
class Organization:
    id: str
    name: str
    user_organization_role: UserOrganizationRole | None = None  # None in case of a global Admin
    image_url: str | None = None
    banner_url: str | None = None
    created_at: str | None = None
    website_url: str | None = None
