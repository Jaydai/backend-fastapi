"""
DTOs for team endpoints
"""

from datetime import datetime

from pydantic import BaseModel, Field

# Request DTOs


class CreateTeamRequestDTO(BaseModel):
    """Request to create a new team"""

    name: str = Field(..., min_length=1, max_length=100, description="Team name")
    description: str | None = Field(None, max_length=500, description="Team description")
    parent_team_id: str | None = Field(None, description="Parent team ID (UUID)")
    color: str = Field(default="#3B82F6", pattern=r"^#[0-9A-Fa-f]{6}$", description="Hex color code")


class UpdateTeamRequestDTO(BaseModel):
    """Request to update an existing team"""

    name: str | None = Field(None, min_length=1, max_length=100, description="Team name")
    description: str | None = Field(None, max_length=500, description="Team description")
    parent_team_id: str | None = Field(None, description="Parent team ID (UUID)")
    color: str | None = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$", description="Hex color code")


class AddTeamMemberRequestDTO(BaseModel):
    """Request to add a user to a team"""

    user_id: str = Field(..., description="User ID to add to the team")
    role: str = Field(default="member", pattern=r"^(member|lead|admin)$", description="User role in the team")


class UpdateTeamMemberRoleRequestDTO(BaseModel):
    """Request to update a team member's role"""

    role: str = Field(..., pattern=r"^(member|lead|admin)$", description="New role for the team member")


# Response DTOs


class TeamMemberDTO(BaseModel):
    """Team member response"""

    user_id: str
    team_id: str
    role: str
    email: str
    name: str | None = None
    joined_at: datetime | None = None


class TeamDTO(BaseModel):
    """Basic team response"""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    parent_team_id: str | None = None
    color: str
    created_at: datetime
    updated_at: datetime
    member_count: int | None = 0


class TeamWithMembersDTO(BaseModel):
    """Team with member details"""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    parent_team_id: str | None = None
    color: str
    created_at: datetime
    updated_at: datetime
    members: list[TeamMemberDTO]
    children: list["TeamWithMembersDTO"] | None = []


class TeamTreeNodeDTO(BaseModel):
    """Hierarchical team tree node"""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    parent_team_id: str | None = None
    color: str
    member_count: int = 0
    depth: int = 0
    path: list[str] = []
    children: list["TeamTreeNodeDTO"] = []


class OrganizationTeamsResponseDTO(BaseModel):
    """Organization teams response with tree structure"""

    organization_id: str
    teams: list[TeamDTO]
    tree: list[TeamTreeNodeDTO]  # Root teams with nested children
    total_teams: int
    total_members: int


class TeamCreatedResponseDTO(BaseModel):
    """Team creation response"""

    team: TeamDTO
    message: str = "Team created successfully"


class TeamUpdatedResponseDTO(BaseModel):
    """Team update response"""

    team: TeamDTO
    message: str = "Team updated successfully"


class TeamDeletedResponseDTO(BaseModel):
    """Team deletion response"""

    team_id: str
    message: str = "Team deleted successfully"


class MemberAddedResponseDTO(BaseModel):
    """Member addition response"""

    member: TeamMemberDTO
    message: str = "Member added to team successfully"


class MemberRemovedResponseDTO(BaseModel):
    """Member removal response"""

    user_id: str
    team_id: int
    message: str = "Member removed from team successfully"
