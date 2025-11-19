from domains.entities import OrganizationInvitation
from dtos import InvitationResponseDTO
from repositories import InvitationRepository
from .user_service import UserService
from supabase import Client
import logging

logger = logging.getLogger(__name__)


class InvitationService:
    @staticmethod
    def get_pending_invitations(client: Client, user_id: str) -> list[InvitationResponseDTO]:
        user_email = UserService.get_email_by_id(client, user_id)
        invitations = InvitationRepository.get_pending_invitations(client, user_email)

        return [
            InvitationResponseDTO(
                id=inv.id,
                invited_email=inv.invited_email,
                inviter_name=inv.inviter_name,
                status=inv.status,
                role=inv.role,
                organization_name=inv.organization_name,
                created_at=inv.created_at
            )
            for inv in invitations
        ]

    @staticmethod
    def get_invitation_by_id(client: Client, invitation_id: str) -> InvitationResponseDTO | None:
        invitation = InvitationRepository.get_invitation_by_id(client, invitation_id)
        if not invitation:
            return None

        return InvitationResponseDTO(
            id=invitation.id,
            invited_email=invitation.invited_email,
            inviter_name=invitation.inviter_name,
            status=invitation.status,
            role=invitation.role,
            organization_name=invitation.organization_name,
            created_at=invitation.created_at
        )

    @staticmethod
    def cancel_invitation(client: Client, invitation_id: str, user_id: str) -> bool:
        invitation = InvitationRepository.get_invitation_by_id(client, invitation_id)
        if not invitation:
            return False

        # Update status to cancelled
        result = InvitationRepository.update_invitation_status(client, invitation, "cancelled")
        return result is not None

    @staticmethod
    def update_invitation_status(client: Client, invitation_id: str, user_id: str, new_status: str) -> InvitationResponseDTO:
        logger.info(f"User {user_id} updating invitation {invitation_id} to status {new_status}")

        invitation = InvitationRepository.get_invitation_by_id(client, invitation_id)
        if not invitation:
            raise ValueError("Invitation not found")

        user_email = UserService.get_email_by_id(client, user_id)
        if invitation.invited_email != user_email:
            raise ValueError("This invitation is not for you")

        if new_status == "accepted":
            if not invitation.can_be_accepted():
                raise ValueError("This invitation cannot be accepted")

            UserService.create_user_organization_role(
                client,
                user_id,
                invitation.organization_id,
                invitation.role
            )
        elif new_status == "declined":
            if not invitation.can_be_declined():
                raise ValueError("This invitation cannot be declined")

        updated_invitation = InvitationRepository.update_invitation_status(
            client,
            invitation,
            new_status
        )

        if not updated_invitation:
            raise ValueError(
                f"Failed to update invitation. It may have already been processed or is no longer valid."
            )

        logger.info(f"User {user_id} successfully updated invitation {invitation_id} to {new_status}")

        return InvitationResponseDTO(
            id=updated_invitation.id,
            invited_email=updated_invitation.invited_email,
            inviter_name=updated_invitation.inviter_name,
            status=updated_invitation.status,
            role=updated_invitation.role,
            organization_name=updated_invitation.organization_name,
            created_at=updated_invitation.created_at
        )
