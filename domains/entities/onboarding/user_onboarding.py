"""
UserOnboarding Entity

Represents the complete onboarding state for a user.
Maps to the users_onboarding table.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

from .onboarding_block import OnboardingBlock
from .use_case import UseCase

OnboardingFlowType = Literal["invited", "create_org", "personal"]
OnboardingStep = Literal[
    "not_started",
    "flow_selection",
    "org_details",
    "personal_chat",
    "workspace_ready",
    "extension_check",
    "completed",
]


@dataclass
class UserOnboarding:
    """
    Complete onboarding state for a user.

    This entity represents all data collected during the onboarding flow,
    including organization info, professional details, and AI-generated content.
    """

    # Primary identifiers
    id: str | None = None
    user_id: str = ""

    # Flow state
    flow_type: OnboardingFlowType | None = None
    current_step: OnboardingStep = "not_started"
    completed_at: datetime | None = None
    dismissed_at: datetime | None = None

    # Organization info (collected during onboarding)
    organization_name: str | None = None
    organization_description: str | None = None
    organization_logo_url: str | None = None
    industry: str | None = None

    # User professional info
    job_title: str | None = None
    job_description: str | None = None
    job_seniority: str | None = None

    # Generated blocks
    context_block: OnboardingBlock | None = None
    role_blocks: list[OnboardingBlock] = field(default_factory=list)
    goal_blocks: list[OnboardingBlock] = field(default_factory=list)
    selected_role_block_ids: list[str] = field(default_factory=list)
    selected_goal_block_ids: list[str] = field(default_factory=list)

    # Use cases
    generated_use_cases: list[UseCase] = field(default_factory=list)
    selected_use_cases: list[str] = field(default_factory=list)

    # Additional data
    ai_dreams: str | None = None
    signup_source: str | None = None
    chat_history: list[dict[str, Any]] | None = None
    chat_summary: str | None = None

    # Extension
    extension_installed: bool = False

    # Timestamps
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def is_completed(self) -> bool:
        """Check if onboarding is fully completed."""
        return self.current_step == "completed" or self.completed_at is not None

    @property
    def is_dismissed(self) -> bool:
        """Check if onboarding was dismissed."""
        return self.dismissed_at is not None

    @property
    def selected_role_blocks(self) -> list[OnboardingBlock]:
        """Get only the selected role blocks."""
        return [b for b in self.role_blocks if b.id in self.selected_role_block_ids]

    @property
    def selected_goal_blocks(self) -> list[OnboardingBlock]:
        """Get only the selected goal blocks."""
        return [b for b in self.goal_blocks if b.id in self.selected_goal_block_ids]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "flow_type": self.flow_type,
            "current_step": self.current_step,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "dismissed_at": self.dismissed_at.isoformat() if self.dismissed_at else None,
            "organization_name": self.organization_name,
            "organization_description": self.organization_description,
            "organization_logo_url": self.organization_logo_url,
            "industry": self.industry,
            "job_title": self.job_title,
            "job_description": self.job_description,
            "job_seniority": self.job_seniority,
            "context_block": self.context_block.to_dict() if self.context_block else None,
            "role_blocks": [b.to_dict() for b in self.role_blocks],
            "goal_blocks": [b.to_dict() for b in self.goal_blocks],
            "selected_role_block_ids": self.selected_role_block_ids,
            "selected_goal_block_ids": self.selected_goal_block_ids,
            "generated_use_cases": [uc.to_dict() for uc in self.generated_use_cases],
            "selected_use_cases": self.selected_use_cases,
            "ai_dreams": self.ai_dreams,
            "signup_source": self.signup_source,
            "extension_installed": self.extension_installed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
