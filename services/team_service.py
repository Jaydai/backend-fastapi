"""
Service layer for team management
"""

from supabase import Client

from dtos.team_dto import OrganizationTeamsResponseDTO, TeamDTO, TeamMemberDTO, TeamTreeNodeDTO
from repositories.team_repository import TeamRepository


class TeamService:
    """Service for team management operations"""

    @staticmethod
    def get_organization_teams(client: Client, organization_id: str) -> OrganizationTeamsResponseDTO:
        """Get all teams for an organization with tree structure"""
        teams = TeamRepository.get_organization_teams(client, organization_id)

        # Get member counts for each team
        for team in teams:
            team.member_count = TeamRepository.get_team_member_count(client, team.id)

        # Build tree structure
        tree = TeamRepository.build_team_tree(teams)

        # Count total members across all teams (unique users)
        all_user_ids = set()
        for team in teams:
            members = TeamRepository.get_team_members(client, team.id)
            all_user_ids.update([m.user_id for m in members])

        # Convert to DTOs
        team_dtos = [
            TeamDTO(
                id=team.id,
                organization_id=team.organization_id,
                name=team.name,
                description=team.description,
                parent_team_id=team.parent_team_id,
                color=team.color,
                created_at=team.created_at,
                updated_at=team.updated_at,
                member_count=team.member_count,
            )
            for team in teams
        ]

        tree_dtos = TeamService._convert_tree_to_dtos(tree)

        return OrganizationTeamsResponseDTO(
            organization_id=organization_id,
            teams=team_dtos,
            tree=tree_dtos,
            total_teams=len(teams),
            total_members=len(all_user_ids),
        )

    @staticmethod
    def get_team_by_id(client: Client, team_id: str) -> TeamDTO | None:
        """Get a specific team by ID"""
        team = TeamRepository.get_team_by_id(client, team_id)
        if not team:
            return None

        member_count = TeamRepository.get_team_member_count(client, team_id)

        return TeamDTO(
            id=team.id,
            organization_id=team.organization_id,
            name=team.name,
            description=team.description,
            parent_team_id=team.parent_team_id,
            color=team.color,
            created_at=team.created_at,
            updated_at=team.updated_at,
            member_count=member_count,
        )

    @staticmethod
    def create_team(
        client: Client,
        organization_id: str,
        name: str,
        description: str | None = None,
        parent_team_id: str | None = None,
        color: str = "#3B82F6",
    ) -> TeamDTO:
        """Create a new team"""
        # Validate parent team exists and belongs to same organization
        if parent_team_id:
            parent_team = TeamRepository.get_team_by_id(client, parent_team_id)
            if not parent_team:
                raise ValueError(f"Parent team {parent_team_id} not found")
            if parent_team.organization_id != organization_id:
                raise ValueError("Parent team must belong to the same organization")

        team = TeamRepository.create_team(client, organization_id, name, description, parent_team_id, color)

        return TeamDTO(
            id=team.id,
            organization_id=team.organization_id,
            name=team.name,
            description=team.description,
            parent_team_id=team.parent_team_id,
            color=team.color,
            created_at=team.created_at,
            updated_at=team.updated_at,
            member_count=0,
        )

    @staticmethod
    def update_team(
        client: Client,
        team_id: str,
        name: str | None = None,
        description: str | None = None,
        parent_team_id: str | None = None,
        color: str | None = None,
    ) -> TeamDTO:
        """Update an existing team"""
        # Validate team exists
        existing_team = TeamRepository.get_team_by_id(client, team_id)
        if not existing_team:
            raise ValueError(f"Team {team_id} not found")

        # Validate parent team if being updated
        if parent_team_id is not None:
            if parent_team_id == team_id:
                raise ValueError("Team cannot be its own parent")

            parent_team = TeamRepository.get_team_by_id(client, parent_team_id)
            if not parent_team:
                raise ValueError(f"Parent team {parent_team_id} not found")
            if parent_team.organization_id != existing_team.organization_id:
                raise ValueError("Parent team must belong to the same organization")

        team = TeamRepository.update_team(client, team_id, name, description, parent_team_id, color)

        member_count = TeamRepository.get_team_member_count(client, team_id)

        return TeamDTO(
            id=team.id,
            organization_id=team.organization_id,
            name=team.name,
            description=team.description,
            parent_team_id=team.parent_team_id,
            color=team.color,
            created_at=team.created_at,
            updated_at=team.updated_at,
            member_count=member_count,
        )

    @staticmethod
    def delete_team(client: Client, team_id: str) -> bool:
        """Delete a team"""
        # Validate team exists
        team = TeamRepository.get_team_by_id(client, team_id)
        if not team:
            raise ValueError(f"Team {team_id} not found")

        return TeamRepository.delete_team(client, team_id)

    @staticmethod
    def get_team_members(client: Client, team_id: str) -> list[TeamMemberDTO]:
        """Get all members of a team"""
        members = TeamRepository.get_team_members(client, team_id)

        return [
            TeamMemberDTO(
                user_id=member.user_id,
                team_id=member.team_id,
                role=member.role,
                email=member.email,
                name=member.name,
                joined_at=member.joined_at,
            )
            for member in members
        ]

    @staticmethod
    def add_user_to_team(client: Client, team_id: str, user_id: str, role: str = "member") -> TeamMemberDTO:
        """Add a user to a team"""
        # Validate team exists
        team = TeamRepository.get_team_by_id(client, team_id)
        if not team:
            raise ValueError(f"Team {team_id} not found")

        # Add user to team
        permission = TeamRepository.add_user_to_team(client, user_id, team_id, role)

        # Get member details
        members = TeamRepository.get_team_members(client, team_id)
        added_member = next((m for m in members if m.user_id == user_id), None)

        if not added_member:
            # Fallback if member details not found
            return TeamMemberDTO(
                user_id=user_id, team_id=team_id, role=role, email="", name=None, joined_at=permission.created_at
            )

        return TeamMemberDTO(
            user_id=added_member.user_id,
            team_id=added_member.team_id,
            role=added_member.role,
            email=added_member.email,
            name=added_member.name,
            joined_at=added_member.joined_at,
        )

    @staticmethod
    def remove_user_from_team(client: Client, team_id: str, user_id: str) -> bool:
        """Remove a user from a team"""
        return TeamRepository.remove_user_from_team(client, user_id, team_id)

    @staticmethod
    def update_user_team_role(client: Client, team_id: str, user_id: str, role: str) -> TeamMemberDTO:
        """Update a user's role in a team"""
        permission = TeamRepository.update_user_team_role(client, user_id, team_id, role)

        # Get updated member details
        members = TeamRepository.get_team_members(client, team_id)
        updated_member = next((m for m in members if m.user_id == user_id), None)

        if not updated_member:
            # Fallback if member details not found
            return TeamMemberDTO(
                user_id=user_id, team_id=team_id, role=role, email="", name=None, joined_at=permission.created_at
            )

        return TeamMemberDTO(
            user_id=updated_member.user_id,
            team_id=updated_member.team_id,
            role=updated_member.role,
            email=updated_member.email,
            name=updated_member.name,
            joined_at=updated_member.joined_at,
        )

    @staticmethod
    def _convert_tree_to_dtos(tree_nodes: list) -> list[TeamTreeNodeDTO]:
        """Convert tree nodes to DTOs recursively"""
        dtos = []
        for node in tree_nodes:
            dto = TeamTreeNodeDTO(
                id=node.id,
                organization_id=node.organization_id,
                name=node.name,
                description=node.description,
                parent_team_id=node.parent_team_id,
                color=node.color,
                member_count=node.member_count,
                depth=node.depth,
                path=node.path,
                children=TeamService._convert_tree_to_dtos(node.children),
            )
            dtos.append(dto)
        return dtos
