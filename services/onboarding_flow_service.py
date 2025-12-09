"""
Onboarding Flow Service

Manages the user onboarding flow state, including:
- Determining flow type (invited, create_org, personal)
- Tracking current step
- Advancing through steps
"""

import logging
from datetime import datetime

from supabase import Client

from dtos.onboarding_dto import (
    OnboardingFlowResponseDTO,
    OnboardingStep,
    PendingInvitationDTO,
    UpdateOnboardingStepDTO,
)
from repositories.onboarding_repository import OnboardingRepository
from services.invitation_service import InvitationService
from services.organization_service import OrganizationService

logger = logging.getLogger(__name__)


# Step order for each flow type
FLOW_STEPS = {
    "invited": ["personal_questions", "extension_check", "completed"],
    "create_org": [
        "org_details",
        "org_billing",
        "org_invite",
        "personal_questions",
        "extension_check",
        "completed",
    ],
    "personal": ["personal_questions", "extension_check", "completed"],
}


class OnboardingFlowService:
    @staticmethod
    def get_onboarding_flow(client: Client, user_id: str) -> OnboardingFlowResponseDTO:
        """
        Get the current onboarding flow state for a user.

        Determines:
        1. If user has pending invitation -> flow_type = 'invited'
        2. If user already has organizations -> skip org creation
        3. Otherwise -> flow_type = None (user must choose)
        """
        # Get current onboarding metadata
        metadata = OnboardingRepository.get_user_metadata(client, user_id)

        # Check if already completed
        has_completed = (
            bool(
                metadata.job_type
                and metadata.job_industry
                and metadata.job_seniority
                and metadata.interests
                and metadata.signup_source
            )
            or metadata.onboarding_dismissed
            or metadata.onboarding_step == "completed"
        )

        if has_completed:
            return OnboardingFlowResponseDTO(
                flow_type=metadata.onboarding_flow_type,
                current_step="completed",
                has_completed_onboarding=True,
                has_extension=metadata.extension_installed,
            )

        # Check for pending invitations
        pending_invitation = None
        try:
            invitations = InvitationService.get_pending_invitations(client, user_id)
            if invitations:
                first_inv = invitations[0]
                pending_invitation = PendingInvitationDTO(
                    id=first_inv.id,
                    organization_id="",  # TODO: Get from invitation
                    organization_name=first_inv.organization_name or "",
                    inviter_name=first_inv.inviter_name,
                    role=first_inv.role,
                )
        except Exception as e:
            logger.warning(f"Error checking pending invitations: {e}")

        # Determine flow type
        flow_type = metadata.onboarding_flow_type

        if pending_invitation and not flow_type:
            flow_type = "invited"

        # If no flow type and not invited, check if user has organizations
        if not flow_type and not pending_invitation:
            try:
                organizations = OrganizationService.get_organizations(client)
                if organizations:
                    # User already has organizations, skip org creation
                    flow_type = "personal"
            except Exception as e:
                logger.warning(f"Error checking organizations: {e}")

        # Determine current step
        current_step = metadata.onboarding_step
        if current_step == "not_started":
            if pending_invitation:
                current_step = "personal_questions"  # Skip to personal for invited users
            elif not flow_type:
                current_step = "flow_selection"
            elif flow_type == "create_org":
                current_step = "org_details"
            else:
                current_step = "personal_questions"

        # Get organization ID if user has one
        organization_id = None
        try:
            organizations = OrganizationService.get_organizations(client)
            if organizations:
                organization_id = organizations[0].id
        except Exception:
            pass

        return OnboardingFlowResponseDTO(
            flow_type=flow_type,
            current_step=current_step,
            pending_invitation=pending_invitation,
            organization_id=organization_id,
            has_extension=metadata.extension_installed,
            has_completed_onboarding=False,
        )

    @staticmethod
    def update_step(
        client: Client, user_id: str, update_data: UpdateOnboardingStepDTO
    ) -> OnboardingFlowResponseDTO:
        """
        Update the current onboarding step.
        """
        update_dict = {"onboarding_step": update_data.step}

        if update_data.flow_type:
            update_dict["onboarding_flow_type"] = update_data.flow_type

        if update_data.step == "completed":
            update_dict["onboarding_completed_at"] = datetime.utcnow().isoformat()

        OnboardingRepository.update_user_metadata(client, user_id, update_dict)

        return OnboardingFlowService.get_onboarding_flow(client, user_id)

    @staticmethod
    def advance_step(client: Client, user_id: str) -> OnboardingFlowResponseDTO:
        """
        Advance to the next step in the current flow.
        """
        current_flow = OnboardingFlowService.get_onboarding_flow(client, user_id)

        if not current_flow.flow_type:
            raise ValueError("Cannot advance step without a flow type")

        flow_steps = FLOW_STEPS.get(current_flow.flow_type, [])
        current_step = current_flow.current_step

        try:
            current_index = flow_steps.index(current_step)
            if current_index < len(flow_steps) - 1:
                next_step = flow_steps[current_index + 1]
            else:
                next_step = "completed"
        except ValueError:
            # Current step not in flow, start from beginning
            next_step = flow_steps[0] if flow_steps else "completed"

        return OnboardingFlowService.update_step(
            client,
            user_id,
            UpdateOnboardingStepDTO(step=next_step),
        )

    @staticmethod
    def complete_onboarding(client: Client, user_id: str) -> OnboardingFlowResponseDTO:
        """
        Mark onboarding as complete.
        """
        update_dict = {
            "onboarding_step": "completed",
            "onboarding_completed_at": datetime.utcnow().isoformat(),
        }

        OnboardingRepository.update_user_metadata(client, user_id, update_dict)

        return OnboardingFlowService.get_onboarding_flow(client, user_id)

    @staticmethod
    def set_extension_installed(client: Client, user_id: str, installed: bool) -> None:
        """
        Update the extension installed status.
        """
        OnboardingRepository.update_user_metadata(
            client, user_id, {"extension_installed": installed}
        )
