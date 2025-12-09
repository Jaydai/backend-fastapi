from typing import Literal

from pydantic import BaseModel


OnboardingFlowType = Literal["invited", "create_org", "personal"]
OnboardingStep = Literal[
    "not_started",
    "flow_selection",
    "org_details",
    "org_billing",
    "org_invite",
    "personal_questions",
    "extension_check",
    "completed",
]


class OnboardingStatusResponseDTO(BaseModel):
    has_completed_onboarding: bool
    job_type: str | None = None
    job_industry: str | None = None
    job_seniority: str | None = None
    job_other_details: str | None = None
    interests: list[str] | None = None
    other_interests: str | None = None
    signup_source: str | None = None
    other_source: str | None = None
    onboarding_dismissed: bool = False
    first_template_created: bool = False
    first_template_used: bool = False
    first_block_created: bool = False
    keyboard_shortcut_used: bool = False


class UpdateOnboardingDTO(BaseModel):
    job_type: str | None = None
    job_industry: str | None = None
    job_seniority: str | None = None
    job_other_details: str | None = None
    interests: list[str] | None = None
    other_interests: str | None = None
    signup_source: str | None = None
    other_source: str | None = None
    onboarding_dismissed: bool | None = None
    first_template_created: bool | None = None
    first_template_used: bool | None = None
    first_block_created: bool | None = None
    keyboard_shortcut_used: bool | None = None


class PendingInvitationDTO(BaseModel):
    """Simplified invitation info for onboarding flow"""

    id: str
    organization_id: str
    organization_name: str
    inviter_name: str
    role: str


class OnboardingFlowResponseDTO(BaseModel):
    """Current onboarding flow state"""

    flow_type: OnboardingFlowType | None = None
    current_step: OnboardingStep = "not_started"
    pending_invitation: PendingInvitationDTO | None = None
    organization_id: str | None = None
    has_extension: bool = False
    # Include status info for convenience
    has_completed_onboarding: bool = False


class UpdateOnboardingStepDTO(BaseModel):
    """Update onboarding step progress"""

    step: OnboardingStep
    flow_type: OnboardingFlowType | None = None


class OnboardingChatMessageDTO(BaseModel):
    """User response in onboarding chat"""

    question_id: str
    user_response: str


class OnboardingChatResponseDTO(BaseModel):
    """AI-processed response for onboarding chat"""

    ai_summary: str | None = None
    extracted_data: dict | None = None
    next_question_id: str | None = None
