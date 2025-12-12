"""
Onboarding DTOs

Data Transfer Objects for onboarding flow API endpoints.
"""

from typing import Literal

from pydantic import BaseModel


# Type definitions
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


# =============================================================================
# Legacy Status DTOs (for backward compatibility)
# =============================================================================


class OnboardingStatusResponseDTO(BaseModel):
    """Legacy onboarding status response."""

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
    """Legacy update onboarding request."""

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


# =============================================================================
# Flow DTOs
# =============================================================================


class PendingInvitationDTO(BaseModel):
    """Simplified invitation info for onboarding flow."""

    id: str
    organization_id: str
    organization_name: str
    inviter_name: str
    role: str


class OnboardingFlowResponseDTO(BaseModel):
    """Current onboarding flow state."""

    flow_type: OnboardingFlowType | None = None
    current_step: OnboardingStep = "not_started"
    pending_invitation: PendingInvitationDTO | None = None
    organization_id: str | None = None
    has_extension: bool = False
    has_completed_onboarding: bool = False


class UpdateOnboardingStepDTO(BaseModel):
    """Update onboarding step progress."""

    step: OnboardingStep
    flow_type: OnboardingFlowType | None = None


# =============================================================================
# Organization Generation DTOs
# =============================================================================


class GenerateOrganizationDescriptionRequestDTO(BaseModel):
    """Request to generate organization description."""

    organization_name: str
    website_url: str | None = None
    linkedin_url: str | None = None
    language: str = "en"


class GenerateOrganizationDescriptionResponseDTO(BaseModel):
    """Response with generated organization description."""

    organization_description: str
    industry: str


# Legacy aliases for backward compatibility
GenerateCompanyDescriptionRequestDTO = GenerateOrganizationDescriptionRequestDTO
GenerateCompanyDescriptionResponseDTO = GenerateOrganizationDescriptionResponseDTO


# =============================================================================
# Job Generation DTOs
# =============================================================================


class GenerateJobDescriptionRequestDTO(BaseModel):
    """Request to generate job description."""

    linkedin_url: str | None = None
    manual_description: str | None = None
    organization_description: str | None = None
    language: str = "en"


class JobDescriptionDTO(BaseModel):
    """A generated job description."""

    job_title: str
    job_description: str
    seniority_level: str  # junior, mid, senior, lead, executive


class GenerateJobDescriptionResponseDTO(BaseModel):
    """Response with generated job description."""

    job_title: str
    job_description: str
    seniority_level: str


# =============================================================================
# Use Case DTOs
# =============================================================================


class AIUseCaseDTO(BaseModel):
    """A generated AI use case."""

    title: str
    description: str
    category: str


class GenerateUseCasesRequestDTO(BaseModel):
    """Request to generate AI use cases based on job."""

    job_title: str
    job_description: str
    organization_description: str | None = None
    industry: str | None = None
    language: str = "en"


class GenerateUseCasesResponseDTO(BaseModel):
    """Response with generated AI use cases."""

    use_cases: list[AIUseCaseDTO]


# =============================================================================
# Block DTOs
# =============================================================================


class BlockDTO(BaseModel):
    """A block that can be used with AI (role, goal, or context)."""

    id: str
    type: Literal["context", "role", "goal"]
    title: str
    description: str
    icon: str | None = None
    category: str | None = None


class GenerateUserBlocksRequestDTO(BaseModel):
    """Request to generate user blocks (context, roles, goals)."""

    job_title: str
    linkedin_url: str | None = None
    manual_description: str | None = None
    organization_name: str | None = None
    organization_description: str | None = None
    industry: str | None = None
    language: str = "en"


class GenerateUserBlocksResponseDTO(BaseModel):
    """Response with generated user blocks."""

    context_block: BlockDTO
    role_blocks: list[BlockDTO]
    goal_blocks: list[BlockDTO]
    job_title: str
    job_description: str
    seniority_level: str


# =============================================================================
# Asset Fetching DTOs
# =============================================================================


class FetchOrganizationLogoRequestDTO(BaseModel):
    """Request to fetch organization logo from website or LinkedIn."""

    website_url: str | None = None
    linkedin_url: str | None = None


class FetchOrganizationLogoResponseDTO(BaseModel):
    """Response with fetched organization logo URL."""

    logo_url: str | None = None


# Legacy aliases
FetchCompanyLogoRequestDTO = FetchOrganizationLogoRequestDTO
FetchCompanyLogoResponseDTO = FetchOrganizationLogoResponseDTO


class FetchProfilePictureRequestDTO(BaseModel):
    """Request to fetch profile picture from LinkedIn."""

    linkedin_url: str | None = None


class FetchProfilePictureResponseDTO(BaseModel):
    """Response with fetched profile picture URL."""

    profile_picture_url: str | None = None


# =============================================================================
# Chat Completion DTOs
# =============================================================================


class OnboardingChatMessageDTO(BaseModel):
    """User response in onboarding chat (legacy)."""

    question_id: str
    user_response: str


class OnboardingChatResponseDTO(BaseModel):
    """AI-processed response for onboarding chat (legacy)."""

    ai_summary: str | None = None
    extracted_data: dict | None = None
    next_question_id: str | None = None


class CompleteOnboardingChatRequestDTO(BaseModel):
    """Request to complete onboarding chat and save data (legacy v1)."""

    company_name: str | None = None
    company_description: str | None = None
    industry: str | None = None
    job_title: str
    job_description: str
    selected_use_cases: list[str] = []
    ai_dreams: str | None = None
    user_message: str | None = None
    signup_source: str


class CompleteOnboardingChatResponseDTO(BaseModel):
    """Response after completing onboarding chat."""

    summary: str
    extracted_data: dict


class CompleteOnboardingChatRequestDTOV2(BaseModel):
    """Request to complete onboarding chat and save data (v2 with blocks)."""

    # Organization info
    organization_name: str | None = None
    organization_logo_url: str | None = None
    organization_description: str | None = None
    industry: str | None = None

    # User info
    profile_picture_url: str | None = None
    job_title: str
    job_description: str
    seniority_level: str | None = None

    # Blocks
    context_block: BlockDTO | None = None
    role_blocks: list[BlockDTO] = []
    goal_blocks: list[BlockDTO] = []
    selected_role_block_ids: list[str] = []
    selected_goal_block_ids: list[str] = []

    # Use cases
    selected_use_cases: list[str] = []

    # Other
    invited_emails: list[str] = []
    ai_dreams: str | None = None
    user_message: str | None = None
    signup_source: str

    # Legacy field aliases for backward compatibility
    @property
    def company_name(self) -> str | None:
        return self.organization_name

    @property
    def company_logo_url(self) -> str | None:
        return self.organization_logo_url

    @property
    def company_description(self) -> str | None:
        return self.organization_description
