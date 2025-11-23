"""
Repository for team-related database operations
"""
from supabase import Client
from typing import Optional
from domains.entities.team_entities import (
    Team,
    UserTeamPermission,
    TeamMember,
    TeamWithMembers,
    TeamTreeNode
)


class TeamRepository:
    """Repository for team operations"""

    @staticmethod
    def get_organization_teams(client: Client, organization_id: str) -> list[Team]:
        """Get all teams for an organization"""
        response = client.table("teams") \
            .select("*") \
            .eq("organization_id", organization_id) \
            .order("name") \
            .execute()

        if not response.data:
            return []

        teams = []
        for row in response.data:
            teams.append(Team(
                id=row["id"],
                organization_id=row["organization_id"],
                name=row["name"],
                description=row.get("description"),
                parent_team_id=row.get("parent_team_id"),
                color=row.get("color", "#3B82F6"),
                created_at=row.get("created_at"),
                updated_at=row.get("updated_at")
            ))

        return teams

    @staticmethod
    def get_team_by_id(client: Client, team_id: int) -> Optional[Team]:
        """Get a specific team by ID"""
        response = client.table("teams") \
            .select("*") \
            .eq("id", team_id) \
            .single() \
            .execute()

        if not response.data:
            return None

        row = response.data
        return Team(
            id=row["id"],
            organization_id=row["organization_id"],
            name=row["name"],
            description=row.get("description"),
            parent_team_id=row.get("parent_team_id"),
            color=row.get("color", "#3B82F6"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at")
        )

    @staticmethod
    def create_team(
        client: Client,
        organization_id: str,
        name: str,
        description: Optional[str] = None,
        parent_team_id: Optional[int] = None,
        color: str = "#3B82F6"
    ) -> Team:
        """Create a new team"""
        response = client.table("teams").insert({
            "organization_id": organization_id,
            "name": name,
            "description": description,
            "parent_team_id": parent_team_id,
            "color": color
        }).execute()

        row = response.data[0]
        return Team(
            id=row["id"],
            organization_id=row["organization_id"],
            name=row["name"],
            description=row.get("description"),
            parent_team_id=row.get("parent_team_id"),
            color=row.get("color", "#3B82F6"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at")
        )

    @staticmethod
    def update_team(
        client: Client,
        team_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        parent_team_id: Optional[int] = None,
        color: Optional[str] = None
    ) -> Team:
        """Update an existing team"""
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if parent_team_id is not None:
            update_data["parent_team_id"] = parent_team_id
        if color is not None:
            update_data["color"] = color

        response = client.table("teams") \
            .update(update_data) \
            .eq("id", team_id) \
            .execute()

        row = response.data[0]
        return Team(
            id=row["id"],
            organization_id=row["organization_id"],
            name=row["name"],
            description=row.get("description"),
            parent_team_id=row.get("parent_team_id"),
            color=row.get("color", "#3B82F6"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at")
        )

    @staticmethod
    def delete_team(client: Client, team_id: int) -> bool:
        """Delete a team (will cascade to children and permissions)"""
        client.table("teams") \
            .delete() \
            .eq("id", team_id) \
            .execute()
        return True

    @staticmethod
    def get_team_members(client: Client, team_id: int) -> list[TeamMember]:
        """Get all members of a team"""
        response = client.table("user_team_permissions") \
            .select("*, users:user_id(email, raw_user_meta_data)") \
            .eq("team_id", team_id) \
            .execute()

        if not response.data:
            return []

        members = []
        for row in response.data:
            user_data = row.get("users", {})
            meta_data = user_data.get("raw_user_meta_data", {})

            members.append(TeamMember(
                user_id=row["user_id"],
                team_id=row["team_id"],
                role=row["role"],
                email=user_data.get("email", ""),
                name=meta_data.get("full_name"),
                joined_at=row.get("created_at")
            ))

        return members

    @staticmethod
    def get_user_teams(client: Client, user_id: str, organization_id: Optional[str] = None) -> list[Team]:
        """Get all teams a user belongs to"""
        query = client.table("user_team_permissions") \
            .select("*, teams(*)") \
            .eq("user_id", user_id)

        response = query.execute()

        if not response.data:
            return []

        teams = []
        for row in response.data:
            team_data = row.get("teams", {})
            if not team_data:
                continue

            # Filter by organization if provided
            if organization_id and team_data.get("organization_id") != organization_id:
                continue

            teams.append(Team(
                id=team_data["id"],
                organization_id=team_data["organization_id"],
                name=team_data["name"],
                description=team_data.get("description"),
                parent_team_id=team_data.get("parent_team_id"),
                color=team_data.get("color", "#3B82F6"),
                created_at=team_data.get("created_at"),
                updated_at=team_data.get("updated_at")
            ))

        return teams

    @staticmethod
    def add_user_to_team(
        client: Client,
        user_id: str,
        team_id: int,
        role: str = "member"
    ) -> UserTeamPermission:
        """Add a user to a team"""
        response = client.table("user_team_permissions").insert({
            "user_id": user_id,
            "team_id": team_id,
            "role": role
        }).execute()

        row = response.data[0]
        return UserTeamPermission(
            id=row["id"],
            user_id=row["user_id"],
            team_id=row["team_id"],
            role=row["role"],
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at")
        )

    @staticmethod
    def remove_user_from_team(client: Client, user_id: str, team_id: int) -> bool:
        """Remove a user from a team"""
        client.table("user_team_permissions") \
            .delete() \
            .eq("user_id", user_id) \
            .eq("team_id", team_id) \
            .execute()
        return True

    @staticmethod
    def update_user_team_role(
        client: Client,
        user_id: str,
        team_id: int,
        role: str
    ) -> UserTeamPermission:
        """Update a user's role in a team"""
        response = client.table("user_team_permissions") \
            .update({"role": role}) \
            .eq("user_id", user_id) \
            .eq("team_id", team_id) \
            .execute()

        row = response.data[0]
        return UserTeamPermission(
            id=row["id"],
            user_id=row["user_id"],
            team_id=row["team_id"],
            role=row["role"],
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at")
        )

    @staticmethod
    def get_team_member_count(client: Client, team_id: int) -> int:
        """Get the number of members in a team"""
        response = client.table("user_team_permissions") \
            .select("id", count="exact") \
            .eq("team_id", team_id) \
            .execute()

        return response.count if response.count else 0

    @staticmethod
    def build_team_tree(teams: list[Team]) -> list[TeamTreeNode]:
        """Build a hierarchical tree structure from a flat list of teams"""
        # Create a map of teams by ID
        team_map = {team.id: team for team in teams}

        # Create tree nodes
        nodes = {}
        for team in teams:
            nodes[team.id] = TeamTreeNode(
                id=team.id,
                organization_id=team.organization_id,
                name=team.name,
                description=team.description,
                parent_team_id=team.parent_team_id,
                color=team.color,
                member_count=team.member_count or 0,
                depth=0,
                path=[],
                children=[]
            )

        # Build the tree structure
        root_nodes = []
        for node in nodes.values():
            if node.parent_team_id is None:
                # This is a root node
                root_nodes.append(node)
            else:
                # Add to parent's children
                parent = nodes.get(node.parent_team_id)
                if parent:
                    parent.children.append(node)
                    node.depth = parent.depth + 1
                    node.path = parent.path + [parent.id]
                else:
                    # Parent not found, treat as root
                    root_nodes.append(node)

        return root_nodes
