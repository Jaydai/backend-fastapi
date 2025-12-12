from dataclasses import dataclass


@dataclass
class OnboardingStatus:
    """Legacy onboarding status for user preferences.

    Note: Onboarding flow state (step, flow_type, completed_at) is now
    stored in users_onboarding table and accessed via OnboardingRepository.
    """
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
    extension_installed: bool = False
