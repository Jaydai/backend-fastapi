import logging

from supabase import Client

from domains.entities import Organization, OrganizationDetail, OrganizationInvitation, OrganizationMember
from dtos import (
    InvitationResponseDTO,
    OrganizationDetailResponseDTO,
    OrganizationMemberResponseDTO,
    OrganizationResponseDTO,
)
from dtos.organization_dto import BulkInviteResponseDTO, CreateOrganizationDTO
from repositories import OrganizationRepository
from services.user_service import UserService

logger = logging.getLogger(__name__)


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

    @staticmethod
    def create_organization(
        client: Client, user_id: str, data: CreateOrganizationDTO
    ) -> OrganizationDetailResponseDTO:
        """
        Create a new organization and set the creator as admin.
        """
        logger.info(f"User {user_id} creating organization: {data.name}")

        organization = OrganizationRepository.create_organization(
            client=client,
            user_id=user_id,
            name=data.name,
            description=data.description,
            image_url=data.image_url,
            website_url=data.website_url,
            org_type=data.type,
        )

        # Get user info to include in response
        user_profile = UserService.get_user_profile(client, user_id)

        members = [
            OrganizationMemberResponseDTO(
                user_id=user_id,
                email=user_profile.email,
                role="admin",
                first_name=user_profile.first_name,
                last_name=user_profile.last_name,
            )
        ]

        logger.info(f"Organization {organization.id} created successfully")

        return OrganizationDetailResponseDTO(
            id=organization.id,
            name=organization.name,
            description={"text": data.description} if data.description else None,
            type=organization.type,
            image_url=organization.image_url,
            banner_url=organization.banner_url,
            website_url=organization.website_url,
            created_at=organization.created_at,
            role="admin",
            members_count=1,
            members=members,
        )

    @staticmethod
    def bulk_invite_members(
        client: Client,
        organization_id: str,
        inviter_id: str,
        emails: list[str],
        role: str = "viewer",
    ) -> BulkInviteResponseDTO:
        """
        Send invitations to multiple emails.
        """
        logger.info(f"User {inviter_id} bulk inviting {len(emails)} users to org {organization_id}")

        # Get inviter info
        user_profile = UserService.get_user_profile(client, inviter_id)
        inviter_name = f"{user_profile.first_name or ''} {user_profile.last_name or ''}".strip()
        if not inviter_name:
            inviter_name = user_profile.email

        # Get organization name
        org = OrganizationRepository.get_organization_by_id(client, organization_id)
        if not org:
            raise ValueError(f"Organization {organization_id} not found")

        result = BulkInviteResponseDTO()

        for email in emails:
            try:
                OrganizationRepository.create_invitation(
                    client=client,
                    organization_id=organization_id,
                    organization_name=org.name,
                    inviter_id=inviter_id,
                    inviter_name=inviter_name,
                    inviter_email=user_profile.email,
                    invited_email=email,
                    role=role,
                )
                result.successful.append(email)
                result.total_invited += 1
            except Exception as e:
                logger.warning(f"Failed to invite {email}: {e}")
                result.failed.append({"email": email, "reason": str(e)})

        logger.info(f"Bulk invite complete: {result.total_invited} successful, {len(result.failed)} failed")
        return result
