"""
Onboarding Flow Service

Manages the user onboarding flow state, including:
- Determining flow type (invited, create_org, personal)
- Tracking current step
- Advancing through steps
- Completing onboarding

Uses the new users_onboarding table via OnboardingRepository.
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
FLOW_STEPS: dict[str, list[str]] = {
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
    """Service for managing onboarding flow state."""

    @staticmethod
    def get_onboarding_flow(client: Client, user_id: str) -> OnboardingFlowResponseDTO:
        """
        Get the current onboarding flow state for a user.

        Determines:
        1. If user has pending invitation -> flow_type = 'invited'
        2. If user already has organizations -> skip org creation
        3. Otherwise -> flow_type = None (user must choose)

        Args:
            client: Supabase client
            user_id: User's UUID

        Returns:
            OnboardingFlowResponseDTO with current state
        """
        # Get or create onboarding record
        onboarding = OnboardingRepository.get_or_create(client, user_id)

        # Check if already completed
        if onboarding.is_completed or onboarding.is_dismissed:
            return OnboardingFlowResponseDTO(
                flow_type=onboarding.flow_type,
                current_step="completed",
                has_completed_onboarding=True,
                has_extension=onboarding.extension_installed,
            )

        # Check for pending invitations
        pending_invitation = OnboardingFlowService._get_pending_invitation(
            client, user_id
        )

        # Determine flow type
        flow_type = onboarding.flow_type

        if pending_invitation and not flow_type:
            flow_type = "invited"

        # If no flow type and not invited, check if user has organizations
        if not flow_type and not pending_invitation:
            flow_type = OnboardingFlowService._check_existing_organizations(client)

        # Determine current step
        current_step = OnboardingFlowService._determine_current_step(
            onboarding.current_step,
            flow_type,
            pending_invitation is not None,
        )

        # Get organization ID if user has one
        organization_id = OnboardingFlowService._get_user_organization_id(client)

        return OnboardingFlowResponseDTO(
            flow_type=flow_type,
            current_step=current_step,
            pending_invitation=pending_invitation,
            organization_id=organization_id,
            has_extension=onboarding.extension_installed,
            has_completed_onboarding=False,
        )

    @staticmethod
    def update_step(
        client: Client, user_id: str, update_data: UpdateOnboardingStepDTO
    ) -> OnboardingFlowResponseDTO:
        """
        Update the current onboarding step.

        Args:
            client: Supabase client
            user_id: User's UUID
            update_data: Step and optional flow type to update

        Returns:
            Updated OnboardingFlowResponseDTO
        """
        OnboardingRepository.update_step(
            client,
            user_id,
            step=update_data.step,
            flow_type=update_data.flow_type,
        )

        return OnboardingFlowService.get_onboarding_flow(client, user_id)

    @staticmethod
    def advance_step(client: Client, user_id: str) -> OnboardingFlowResponseDTO:
        """
        Advance to the next step in the current flow.

        Args:
            client: Supabase client
            user_id: User's UUID

        Returns:
            Updated OnboardingFlowResponseDTO

        Raises:
            ValueError: If no flow type is set
        """
        current_flow = OnboardingFlowService.get_onboarding_flow(client, user_id)

        if not current_flow.flow_type:
            raise ValueError("Cannot advance step without a flow type")

        flow_steps = FLOW_STEPS.get(current_flow.flow_type, [])
        current_step = current_flow.current_step

        next_step = OnboardingFlowService._get_next_step(flow_steps, current_step)

        return OnboardingFlowService.update_step(
            client,
            user_id,
            UpdateOnboardingStepDTO(step=next_step),
        )

    @staticmethod
    def complete_onboarding(client: Client, user_id: str) -> OnboardingFlowResponseDTO:
        """
        Mark onboarding as complete.

        Args:
            client: Supabase client
            user_id: User's UUID

        Returns:
            Updated OnboardingFlowResponseDTO
        """
        OnboardingRepository.complete(client, user_id)
        return OnboardingFlowService.get_onboarding_flow(client, user_id)

    @staticmethod
    def dismiss_onboarding(client: Client, user_id: str) -> OnboardingFlowResponseDTO:
        """
        Dismiss onboarding (user chose to skip).

        Args:
            client: Supabase client
            user_id: User's UUID

        Returns:
            Updated OnboardingFlowResponseDTO
        """
        OnboardingRepository.dismiss(client, user_id)
        return OnboardingFlowService.get_onboarding_flow(client, user_id)

    @staticmethod
    def set_extension_installed(
        client: Client, user_id: str, installed: bool = True
    ) -> None:
        """
        Update the extension installed status.

        Args:
            client: Supabase client
            user_id: User's UUID
            installed: Whether extension is installed
        """
        OnboardingRepository.set_extension_installed(client, user_id, installed)

    # =========================================================================
    # Private helper methods
    # =========================================================================

    @staticmethod
    def _get_pending_invitation(
        client: Client, user_id: str
    ) -> PendingInvitationDTO | None:
        """Get the first pending invitation for the user."""
        try:
            invitations = InvitationService.get_pending_invitations(client, user_id)
            if invitations:
                first_inv = invitations[0]
                return PendingInvitationDTO(
                    id=first_inv.id,
                    organization_id=getattr(first_inv, "organization_id", ""),
                    organization_name=first_inv.organization_name or "",
                    inviter_name=first_inv.inviter_name,
                    role=first_inv.role,
                )
        except Exception as e:
            logger.warning(f"Error checking pending invitations: {e}")
        return None

    @staticmethod
    def _check_existing_organizations(client: Client) -> str | None:
        """Check if user has existing organizations, return 'personal' if so."""
        try:
            organizations = OrganizationService.get_organizations(client)
            if organizations:
                return "personal"
        except Exception as e:
            logger.warning(f"Error checking organizations: {e}")
        return None

    @staticmethod
    def _get_user_organization_id(client: Client) -> str | None:
        """Get the user's first organization ID if any."""
        try:
            organizations = OrganizationService.get_organizations(client)
            if organizations:
                return organizations[0].id
        except Exception:
            pass
        return None

    @staticmethod
    def _determine_current_step(
        stored_step: str,
        flow_type: str | None,
        has_pending_invitation: bool,
    ) -> OnboardingStep:
        """Determine the appropriate current step based on state."""
        if stored_step != "not_started":
            return stored_step

        if has_pending_invitation:
            return "personal_questions"
        elif not flow_type:
            return "flow_selection"
        elif flow_type == "create_org":
            return "org_details"
        else:
            return "personal_questions"

    @staticmethod
    def _get_next_step(flow_steps: list[str], current_step: str) -> OnboardingStep:
        """Get the next step in the flow."""
        try:
            current_index = flow_steps.index(current_step)
            if current_index < len(flow_steps) - 1:
                return flow_steps[current_index + 1]
            else:
                return "completed"
        except ValueError:
            # Current step not in flow, start from beginning
            return flow_steps[0] if flow_steps else "completed"
