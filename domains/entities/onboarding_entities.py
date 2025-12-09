from dataclasses import dataclass
from datetime import datetime


@dataclass
class OnboardingStatus:
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
    # New fields for onboarding flow
    onboarding_step: str = "not_started"
    onboarding_flow_type: str | None = None
    onboarding_completed_at: datetime | None = None
    extension_installed: bool = False
