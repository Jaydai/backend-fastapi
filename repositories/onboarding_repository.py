from supabase import Client
from domains.entities.onboarding_entities import OnboardingStatus

class OnboardingRepository:
    @staticmethod
    def get_user_metadata(client: Client, user_id: str) -> OnboardingStatus:
        response = client.table("users_metadata") \
            .select("job_type, job_industry, job_seniority, interests, signup_source, onboarding_dismissed, first_template_created, first_template_used, first_block_created, keyboard_shortcut_used") \
            .eq("user_id", user_id) \
            .single() \
            .execute()

        if not response.data:
            return OnboardingStatus()

        data = response.data
        return OnboardingStatus(
            job_type=data.get("job_type"),
            job_industry=data.get("job_industry"),
            job_seniority=data.get("job_seniority"),
            interests=data.get("interests"),
            signup_source=data.get("signup_source"),
            onboarding_dismissed=data.get("onboarding_dismissed", False),
            first_template_created=data.get("first_template_created", False),
            first_template_used=data.get("first_template_used", False),
            first_block_created=data.get("first_block_created", False),
            keyboard_shortcut_used=data.get("keyboard_shortcut_used", False)
        )

    @staticmethod
    def update_user_metadata(client: Client, user_id: str, metadata: dict) -> dict:
        existing = client.table("users_metadata") \
            .select("id") \
            .eq("user_id", user_id) \
            .execute()

        if existing.data:
            response = client.table("users_metadata") \
                .update(metadata) \
                .eq("user_id", user_id) \
                .execute()
        else:
            metadata["user_id"] = user_id
            response = client.table("users_metadata") \
                .insert(metadata) \
                .execute()

        if not response.data:
            raise ValueError("Failed to update user metadata")

        return response.data[0]
