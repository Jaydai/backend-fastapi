from domains.entities import OrganizationInvitation
from dtos import InvitationResponseDTO
from repositories import InvitationRepository
from .user_service import UserService
from supabase import Client
import logging

logger = logging.getLogger(__name__)


class InvitationService:
    @staticmethod
    def accept_invitation(client: Client, invitation_id: str, user_id: str) -> InvitationResponseDTO:
        logger.info(f"User {user_id} accepting invitation {invitation_id}")

        invitation: OrganizationInvitation = InvitationRepository.get_invitation_by_id(client, invitation_id)

        if not invitation:
            raise ValueError("Invitation not found")

        user_email = UserService.get_email_by_id(client, user_id)
        if invitation.invited_email != user_email:
            raise ValueError("This invitation is not for you")

        if not invitation.can_be_accepted():
            raise ValueError("This invitation cannot be accepted")
        
        UserService.create_user_organization_role(
            client,
            user_id,
            invitation.organization_id,
            invitation.role
        )
        accepted_invitation = InvitationRepository.accept_invitation(
            client,
            invitation
        )
        if not accepted_invitation:
            raise ValueError(
                "Failed to accept invitation. It may have already been processed or is no longer valid."
            )

        logger.info(f"User {user_id} successfully accepted invitation {invitation_id}")

        return InvitationResponseDTO(
            id=accepted_invitation.id,
            invited_email=accepted_invitation.invited_email,
            inviter_name=accepted_invitation.inviter_name,
            status=accepted_invitation.status,
            role=accepted_invitation.role,
            organization_name=accepted_invitation.organization_name,
            created_at=accepted_invitation.created_at
        )

    @staticmethod
    def decline_invitation(client: Client, invitation_id: str, user_id: str) -> InvitationResponseDTO:
        logger.info(f"User {user_id} declining invitation {invitation_id}")

        invitation = InvitationRepository.get_invitation_by_id(client, invitation_id)
        if not invitation:
            raise ValueError("Invitation not found")

        user_email = UserService.get_email_by_id(client, user_id)
        if invitation.invited_email != user_email:
            raise ValueError("This invitation is not for you")

        if not invitation.can_be_declined():
            raise ValueError("This invitation cannot be declined")
        
        declined_invitation = InvitationRepository.decline_invitation(
            client,
            invitation
        )

        if not declined_invitation:
            raise ValueError(
                "Failed to decline invitation. It may have already been processed or is no longer valid."
            )

        logger.info(f"User {user_id} successfully declined invitation {invitation_id}")

        return InvitationResponseDTO(
            id=declined_invitation.id,
            invited_email=declined_invitation.invited_email,
            inviter_name=declined_invitation.inviter_name,
            status=declined_invitation.status,
            role=declined_invitation.role,
            organization_name=declined_invitation.organization_name,
            created_at=declined_invitation.created_at
        )
