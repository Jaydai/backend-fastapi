from pydantic import BaseModel, field_validator
from domains.enums import RoleEnum


class OrganizationResponseDTO(BaseModel):
    id: str
    name: str
    role: str | None = None
    image_url: str | None = None
    banner_url: str | None = None
    created_at: str | None = None
    website_url: str | None = None


class OrganizationMemberResponseDTO(BaseModel):
    user_id: str
    email: str
    role: str
    first_name: str | None = None
    last_name: str | None = None


class OrganizationDetailResponseDTO(BaseModel):
    id: str
    name: str
    description: dict | None = None  # JSONB field
    image_url: str | None = None
    banner_url: str | None = None
    website_url: str | None = None
    created_at: str | None = None
    role: str | None = None  # Current user's role in this organization
    members_count: int = 0  # Total number of members
    members: list[OrganizationMemberResponseDTO] = []  # All members with their roles


class UpdateMemberRoleDTO(BaseModel):
    role: str

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        valid_roles = [role.value for role in RoleEnum]
        if v not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        return v


class InvitationResponseDTO(BaseModel):
    id: str
    invited_email: str
    inviter_name: str
    status: str
    role: str
    organization_name: str | None = None
    created_at: str | None = None


class UpdateInvitationStatusDTO(BaseModel):
    status: str

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        valid_statuses = ["accepted", "declined"]
        if v not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        return v
