from typing import Literal

from pydantic import BaseModel, EmailStr, field_validator

from domains.enums import RoleEnum

OrganizationType = Literal["company", "standard"]


class CreateOrganizationDTO(BaseModel):
    """DTO for creating a new organization"""
    name: str
    description: str | None = None
    image_url: str | None = None
    website_url: str | None = None
    type: OrganizationType = "company"


class BulkInviteDTO(BaseModel):
    """DTO for bulk inviting members to an organization"""

    emails: list[EmailStr]
    role: str = "viewer"

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        valid_roles = [role.value for role in RoleEnum]
        if v not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        return v

    @field_validator("emails")
    @classmethod
    def validate_emails(cls, v: list) -> list:
        if len(v) == 0:
            raise ValueError("At least one email is required")
        if len(v) > 50:
            raise ValueError("Maximum 50 emails allowed per request")
        return v


class BulkInviteResponseDTO(BaseModel):
    """Response for bulk invite operation"""

    successful: list[str] = []  # Successfully invited emails
    failed: list[dict] = []  # Failed emails with reasons
    total_invited: int = 0


class OrganizationResponseDTO(BaseModel):
    id: str
    name: str
    role: str | None = None
    type: OrganizationType = "standard"
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
    type: OrganizationType = "standard"
    image_url: str | None = None
    banner_url: str | None = None
    website_url: str | None = None
    created_at: str | None = None
    role: str | None = None  # Current user's role in this organization
    members_count: int = 0  # Total number of members
    members: list[OrganizationMemberResponseDTO] = []  # All members with their roles


class UpdateMemberRoleDTO(BaseModel):
    role: str

    @field_validator("role")
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

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        valid_statuses = ["accepted", "declined"]
        if v not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        return v
