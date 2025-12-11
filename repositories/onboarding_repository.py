from supabase import Client

from domains.entities.onboarding_entities import OnboardingStatus


class OnboardingRepository:
    @staticmethod
    def get_user_metadata(client: Client, user_id: str) -> OnboardingStatus:
        response = (
            client.table("users_metadata")
            .select(
                "job_type, job_industry, job_seniority, interests, signup_source, "
                "onboarding_dismissed, first_template_created, first_template_used, "
                "first_block_created, keyboard_shortcut_used, onboarding_step, "
                "onboarding_flow_type, onboarding_completed_at, extension_installed"
            )
            .eq("user_id", user_id)
            .single()
            .execute()
        )

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
            keyboard_shortcut_used=data.get("keyboard_shortcut_used", False),
            onboarding_step=data.get("onboarding_step", "not_started"),
            onboarding_flow_type=data.get("onboarding_flow_type"),
            onboarding_completed_at=data.get("onboarding_completed_at"),
            extension_installed=data.get("extension_installed", False),
        )

    @staticmethod
    def update_user_metadata(client: Client, user_id: str, metadata: dict) -> dict:
        existing = client.table("users_metadata").select("id").eq("user_id", user_id).execute()

        if existing.data:
            response = client.table("users_metadata").update(metadata).eq("user_id", user_id).execute()
        else:
            metadata["user_id"] = user_id
            response = client.table("users_metadata").insert(metadata).execute()

        if not response.data:
            raise ValueError("Failed to update user metadata")

        return response.data[0]

    @staticmethod
    def save_chat_data(
        client: Client,
        user_id: str,
        chat_history: list[dict],
        chat_summary: str | None,
        extracted_data: dict | None,
    ) -> dict:
        """
        Save onboarding chat data to users_metadata.

        Args:
            client: Supabase client
            user_id: User's ID
            chat_history: Full conversation history
            chat_summary: AI-generated summary
            extracted_data: Extracted structured data (job_type, interests, etc.)
        """
        import json

        # Build the update payload
        update_data: dict = {
            "onboarding_chat_history": json.dumps(chat_history),
        }

        if chat_summary:
            update_data["onboarding_chat_summary"] = chat_summary

        # Also update extracted fields if present
        if extracted_data:
            field_mapping = {
                "job_type": "job_type",
                "job_industry": "job_industry",
                "job_seniority": "job_seniority",
                "interests": "interests",
            }
            for source_field, target_field in field_mapping.items():
                if source_field in extracted_data and extracted_data[source_field]:
                    update_data[target_field] = extracted_data[source_field]

        return OnboardingRepository.update_user_metadata(client, user_id, update_data)
