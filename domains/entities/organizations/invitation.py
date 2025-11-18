from dataclasses import dataclass
from ..permission_entities import UserOrganizationRole


@dataclass
class OrganizationInvitation:
    id: str
    invited_email: str
    inviter_email: str
    inviter_name: str
    status: str  # TODO ? pending, accepted, declined, cancelled
    organization_id: str
    role: UserOrganizationRole
    organization_name: str | None = None
    created_at: str | None = None

    def can_be_accepted(self) -> bool:
        return self.status in ["pending", "joined_pending"]

    def can_be_declined(self) -> bool:
        return self.status in ["pending", "joined_pending"]