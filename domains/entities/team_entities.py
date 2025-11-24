"""
Domain entities for team functionality
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Team:
    """Team entity"""
    id: str  # UUID
    organization_id: str  # UUID
    name: str
    description: str | None = None
    parent_team_id: str | None = None  # UUID
    color: str = '#3B82F6'
    created_at: datetime | None = None
    updated_at: datetime | None = None

    # Computed fields (not from database)
    member_count: int | None = None
    children: list['Team'] | None = None

    def __post_init__(self):
        if self.children is None:
            self.children = []


@dataclass
class UserTeamPermission:
    """User team permission entity"""
    id: str  # UUID
    user_id: str  # UUID
    team_id: str  # UUID
    role: str  # 'member', 'lead', 'admin'
    created_at: datetime | None = None
    updated_at: datetime | None = None

    # Optional user details (for joined queries)
    user_email: str | None = None
    user_name: str | None = None


@dataclass
class TeamMember:
    """Team member with user details"""
    user_id: str  # UUID
    team_id: str  # UUID
    role: str
    email: str
    name: str | None = None
    joined_at: datetime | None = None


@dataclass
class TeamWithMembers:
    """Team with member details"""
    id: str  # UUID
    organization_id: str  # UUID
    name: str
    description: str | None = None
    parent_team_id: str | None = None  # UUID
    color: str = '#3B82F6'
    created_at: datetime | None = None
    updated_at: datetime | None = None
    members: list[TeamMember] = None
    children: list['TeamWithMembers'] | None = None

    def __post_init__(self):
        if self.members is None:
            self.members = []
        if self.children is None:
            self.children = []


@dataclass
class TeamTreeNode:
    """Hierarchical team tree node"""
    id: str  # UUID
    organization_id: str  # UUID
    name: str
    description: str | None = None
    parent_team_id: str | None = None  # UUID
    color: str = '#3B82F6'
    member_count: int = 0
    depth: int = 0
    path: list[str] = None  # Path from root to this node (UUIDs)
    children: list['TeamTreeNode'] = None

    def __post_init__(self):
        if self.path is None:
            self.path = []
        if self.children is None:
            self.children = []
