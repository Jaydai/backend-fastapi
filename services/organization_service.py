from domains.entities import Organization, OrganizationDetail, OrganizationInvitation, OrganizationMember
from dtos import (
    InvitationResponseDTO,
    OrganizationDetailResponseDTO,
    OrganizationMemberResponseDTO,
    OrganizationResponseDTO,
)
from repositories import OrganizationRepository
from supabase import Client


class OrganizationService:
    @staticmethod
    def get_organizations(client: Client) -> list[OrganizationResponseDTO]:
        organizations: list[Organization] = OrganizationRepository.get_organizations_with_roles(client)
        return [
            OrganizationResponseDTO(
                id=org.id,
                name=org.name,
                role=org.user_organization_role.role if org.user_organization_role else None,
                image_url=org.image_url,
                banner_url=org.banner_url,
                created_at=org.created_at,
                website_url=org.website_url,
            )
            for org in organizations
        ]

    @staticmethod
    def get_organization_members(client: Client, organization_id: str) -> list[OrganizationMemberResponseDTO]:
        members: list[OrganizationMember] = OrganizationRepository.get_organization_members(client, organization_id)

        return [
            OrganizationMemberResponseDTO(
                user_id=member.user_id,
                email=member.email,
                role=member.role,
                first_name=member.first_name,
                last_name=member.last_name,
            )
            for member in members
        ]

    @staticmethod
    def update_member_role(
        client: Client, organization_id: str, user_id: str, new_role: str
    ) -> OrganizationMemberResponseDTO:
        # TODO: règles par rapport à "est ce que on peut ne plus avoir d'admin" ou "est ce qu'on peut se changer son propre role?"
        updated_member: OrganizationMember | None = OrganizationRepository.update_member_role(
            client, organization_id, user_id, new_role
        )

        if not updated_member:
            raise ValueError(
                f"Failed to update role for user {user_id} in organization {organization_id}. "
                "Member may not exist or you may not have permission."
            )

        return OrganizationMemberResponseDTO(
            user_id=updated_member.user_id,
            email=updated_member.email,
            role=updated_member.role,
            first_name=updated_member.first_name,
            last_name=updated_member.last_name,
        )

    @staticmethod
    def remove_member(client: Client, organization_id: str, user_id: str) -> None:
        # TODO: est ce qu'on peut se supprimer soi même? est ce qu'on peut supprimer le dernier admin?
        success = OrganizationRepository.remove_member(client, organization_id, user_id)

        if not success:
            raise ValueError(
                f"Failed to remove user {user_id} from organization {organization_id}. "
                "Member may not exist or you may not have permission."
            )

    @staticmethod
    def get_organization_by_id(client: Client, organization_id: str) -> OrganizationDetailResponseDTO:
        organization_detail: OrganizationDetail | None = OrganizationRepository.get_organization_by_id(
            client, organization_id
        )

        if not organization_detail:
            raise ValueError(f"Organization {organization_id} not found or you don't have permission to access it.")

        members_dto = [
            OrganizationMemberResponseDTO(
                user_id=member.user_id,
                email=member.email,
                role=member.role,
                first_name=member.first_name,
                last_name=member.last_name,
            )
            for member in organization_detail.members
        ]

        return OrganizationDetailResponseDTO(
            id=organization_detail.id,
            name=organization_detail.name,
            description=organization_detail.description,
            image_url=organization_detail.image_url,
            banner_url=organization_detail.banner_url,
            website_url=organization_detail.website_url,
            created_at=organization_detail.created_at,
            role=organization_detail.user_role,
            members_count=len(organization_detail.members),
            members=members_dto,
        )

    @staticmethod
    def get_organization_invitations(client: Client, organization_id: str) -> list[InvitationResponseDTO]:
        invitations: list[OrganizationInvitation] = OrganizationRepository.get_organization_invitations(
            client, organization_id
        )

        return [
            InvitationResponseDTO(
                id=invitation.id,
                invited_email=invitation.invited_email,
                inviter_name=invitation.inviter_name,
                status=invitation.status,
                role=invitation.role,
                organization_name=invitation.organization_name,
                created_at=invitation.created_at,
            )
            for invitation in invitations
        ]
