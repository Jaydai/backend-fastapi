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
    description: Optional[str] = None
    parent_team_id: Optional[str] = None  # UUID
    color: str = '#3B82F6'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Computed fields (not from database)
    member_count: Optional[int] = None
    children: Optional[list['Team']] = None

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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Optional user details (for joined queries)
    user_email: Optional[str] = None
    user_name: Optional[str] = None


@dataclass
class TeamMember:
    """Team member with user details"""
    user_id: str  # UUID
    team_id: str  # UUID
    role: str
    email: str
    name: Optional[str] = None
    joined_at: Optional[datetime] = None


@dataclass
class TeamWithMembers:
    """Team with member details"""
    id: str  # UUID
    organization_id: str  # UUID
    name: str
    description: Optional[str] = None
    parent_team_id: Optional[str] = None  # UUID
    color: str = '#3B82F6'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    members: list[TeamMember] = None
    children: Optional[list['TeamWithMembers']] = None

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
    description: Optional[str] = None
    parent_team_id: Optional[str] = None  # UUID
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
