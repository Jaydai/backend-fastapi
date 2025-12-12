from supabase import Client

from dtos.onboarding_dto import OnboardingStatusResponseDTO, UpdateOnboardingDTO
from repositories.onboarding_repository import OnboardingRepositoryLegacy


class OnboardingService:
    """Service for legacy onboarding status (user preferences).

    Note: For the new onboarding flow state, use OnboardingFlowService.
    """

    @staticmethod
    def get_onboarding_status(client: Client, user_id: str) -> OnboardingStatusResponseDTO:
        entity = OnboardingRepositoryLegacy.get_user_metadata(client, user_id)

        has_completed = (
            bool(
                entity.job_type
                and entity.job_industry
                and entity.job_seniority
                and entity.interests
                and entity.signup_source
            )
            or entity.onboarding_dismissed
        )

        return OnboardingStatusResponseDTO(
            has_completed_onboarding=has_completed,
            job_type=entity.job_type,
            job_industry=entity.job_industry,
            job_seniority=entity.job_seniority,
            job_other_details=entity.job_other_details,
            interests=entity.interests,
            other_interests=entity.other_interests,
            signup_source=entity.signup_source,
            other_source=entity.other_source,
            onboarding_dismissed=entity.onboarding_dismissed,
            first_template_created=entity.first_template_created,
            first_template_used=entity.first_template_used,
            first_block_created=entity.first_block_created,
            keyboard_shortcut_used=entity.keyboard_shortcut_used,
        )

    @staticmethod
    def update_onboarding(
        client: Client, user_id: str, update_data: UpdateOnboardingDTO
    ) -> OnboardingStatusResponseDTO:
        update_dict = {}
        for field, value in update_data.model_dump(exclude_none=True).items():
            update_dict[field] = value

        if not update_dict:
            raise ValueError("No fields to update")

        OnboardingRepositoryLegacy.update_user_metadata(client, user_id, update_dict)

        return OnboardingService.get_onboarding_status(client, user_id)
