"""
Onboarding Repository

Handles all database operations for the users_onboarding table.
All methods follow async patterns as per coding standards.
"""

import json
import logging
from datetime import datetime
from typing import Any

from supabase import Client

from domains.entities.onboarding import (
    OnboardingBlock,
    UseCase,
    UserOnboarding,
)

logger = logging.getLogger(__name__)

TABLE_NAME = "users_onboarding"


class OnboardingRepository:
    """Repository for users_onboarding table operations."""

    @staticmethod
    def get_by_user_id(client: Client, user_id: str) -> UserOnboarding | None:
        """
        Fetch onboarding record by user ID.

        Args:
            client: Supabase client
            user_id: User's UUID

        Returns:
            UserOnboarding entity or None if not found
        """
        try:
            response = (
                client.table(TABLE_NAME)
                .select("*")
                .eq("user_id", user_id)
                .maybe_single()
                .execute()
            )

            # Handle case where response is None or has no data
            if response is None or not response.data:
                return None

            return OnboardingRepository._map_to_entity(response.data)
        except Exception as e:
            # Log error but return None instead of raising
            # This allows graceful degradation when table doesn't exist yet
            logger.warning(f"Could not fetch onboarding for user {user_id}: {e}")
            return None

    @staticmethod
    def create(client: Client, user_id: str) -> UserOnboarding:
        """
        Create a new onboarding record for a user.

        Args:
            client: Supabase client
            user_id: User's UUID

        Returns:
            Created UserOnboarding entity

        Raises:
            ValueError: If creation fails
        """
        data = {
            "user_id": user_id,
            "current_step": "not_started",
        }

        response = client.table(TABLE_NAME).insert(data).execute()

        if not response.data:
            raise ValueError("Failed to create onboarding record")

        logger.info(f"Created onboarding record for user {user_id}")
        return OnboardingRepository._map_to_entity(response.data[0])

    @staticmethod
    def get_or_create(client: Client, user_id: str) -> UserOnboarding:
        """
        Get existing or create new onboarding record.

        Args:
            client: Supabase client
            user_id: User's UUID

        Returns:
            UserOnboarding entity
        """
        existing = OnboardingRepository.get_by_user_id(client, user_id)
        if existing:
            return existing
        return OnboardingRepository.create(client, user_id)

    @staticmethod
    def update(
        client: Client,
        user_id: str,
        updates: dict[str, Any],
    ) -> UserOnboarding:
        """
        Update onboarding record.

        Args:
            client: Supabase client
            user_id: User's UUID
            updates: Dictionary of fields to update

        Returns:
            Updated UserOnboarding entity

        Raises:
            ValueError: If update fails
        """
        # Add updated_at timestamp
        updates["updated_at"] = datetime.utcnow().isoformat()

        response = (
            client.table(TABLE_NAME)
            .update(updates)
            .eq("user_id", user_id)
            .execute()
        )

        if not response.data:
            raise ValueError(f"Failed to update onboarding for user {user_id}")

        logger.info(f"Updated onboarding for user {user_id}: {list(updates.keys())}")
        return OnboardingRepository._map_to_entity(response.data[0])

    @staticmethod
    def update_step(
        client: Client,
        user_id: str,
        step: str,
        flow_type: str | None = None,
    ) -> UserOnboarding:
        """
        Update the current step and optionally flow type.

        Args:
            client: Supabase client
            user_id: User's UUID
            step: New step value
            flow_type: Optional flow type

        Returns:
            Updated UserOnboarding entity
        """
        updates: dict[str, Any] = {"current_step": step}

        if flow_type:
            updates["flow_type"] = flow_type

        if step == "completed":
            updates["completed_at"] = datetime.utcnow().isoformat()

        return OnboardingRepository.update(client, user_id, updates)

    @staticmethod
    def dismiss(client: Client, user_id: str) -> UserOnboarding:
        """
        Mark onboarding as dismissed.

        Args:
            client: Supabase client
            user_id: User's UUID

        Returns:
            Updated UserOnboarding entity
        """
        return OnboardingRepository.update(
            client,
            user_id,
            {"dismissed_at": datetime.utcnow().isoformat()},
        )

    @staticmethod
    def save_organization_info(
        client: Client,
        user_id: str,
        organization_name: str | None,
        organization_description: str | None,
        organization_logo_url: str | None,
        industry: str | None,
    ) -> UserOnboarding:
        """
        Save organization info from onboarding.

        Args:
            client: Supabase client
            user_id: User's UUID
            organization_name: Organization name
            organization_description: AI-generated description
            organization_logo_url: Logo URL
            industry: Industry category

        Returns:
            Updated UserOnboarding entity
        """
        updates = {
            k: v
            for k, v in {
                "organization_name": organization_name,
                "organization_description": organization_description,
                "organization_logo_url": organization_logo_url,
                "industry": industry,
            }.items()
            if v is not None
        }

        return OnboardingRepository.update(client, user_id, updates)

    @staticmethod
    def save_professional_info(
        client: Client,
        user_id: str,
        job_title: str | None,
        job_description: str | None,
        job_seniority: str | None,
    ) -> UserOnboarding:
        """
        Save user's professional info from onboarding.

        Args:
            client: Supabase client
            user_id: User's UUID
            job_title: Job title
            job_description: AI-generated job description
            job_seniority: Seniority level

        Returns:
            Updated UserOnboarding entity
        """
        updates = {
            k: v
            for k, v in {
                "job_title": job_title,
                "job_description": job_description,
                "job_seniority": job_seniority,
            }.items()
            if v is not None
        }

        return OnboardingRepository.update(client, user_id, updates)

    @staticmethod
    def save_blocks(
        client: Client,
        user_id: str,
        context_block: dict[str, Any] | None,
        role_blocks: list[dict[str, Any]],
        goal_blocks: list[dict[str, Any]],
        selected_role_block_ids: list[str],
        selected_goal_block_ids: list[str],
    ) -> UserOnboarding:
        """
        Save generated blocks from onboarding chat.

        Args:
            client: Supabase client
            user_id: User's UUID
            context_block: Context block dict
            role_blocks: List of role block dicts
            goal_blocks: List of goal block dicts
            selected_role_block_ids: IDs of selected role blocks
            selected_goal_block_ids: IDs of selected goal blocks

        Returns:
            Updated UserOnboarding entity
        """
        updates = {
            "context_block": context_block,
            "role_blocks": role_blocks,
            "goal_blocks": goal_blocks,
            "selected_role_block_ids": selected_role_block_ids,
            "selected_goal_block_ids": selected_goal_block_ids,
        }

        return OnboardingRepository.update(client, user_id, updates)

    @staticmethod
    def save_use_cases(
        client: Client,
        user_id: str,
        generated_use_cases: list[dict[str, Any]],
        selected_use_cases: list[str],
    ) -> UserOnboarding:
        """
        Save generated use cases from onboarding.

        Args:
            client: Supabase client
            user_id: User's UUID
            generated_use_cases: List of generated use case dicts
            selected_use_cases: Titles of selected use cases

        Returns:
            Updated UserOnboarding entity
        """
        return OnboardingRepository.update(
            client,
            user_id,
            {
                "generated_use_cases": generated_use_cases,
                "selected_use_cases": selected_use_cases,
            },
        )

    @staticmethod
    def save_chat_completion(
        client: Client,
        user_id: str,
        data: dict[str, Any],
    ) -> UserOnboarding:
        """
        Save all data from chat completion.

        This is the main method called when the onboarding chat is completed.
        It saves all collected data in one update.

        Args:
            client: Supabase client
            user_id: User's UUID
            data: Dictionary with all chat completion data

        Returns:
            Updated UserOnboarding entity
        """
        updates: dict[str, Any] = {}

        # Organization info
        if data.get("organization_name"):
            updates["organization_name"] = data["organization_name"]
        if data.get("organization_description"):
            updates["organization_description"] = data["organization_description"]
        if data.get("organization_logo_url"):
            updates["organization_logo_url"] = data["organization_logo_url"]
        if data.get("industry"):
            updates["industry"] = data["industry"]

        # Professional info
        if data.get("job_title"):
            updates["job_title"] = data["job_title"]
        if data.get("job_description"):
            updates["job_description"] = data["job_description"]
        if data.get("job_seniority"):
            updates["job_seniority"] = data["job_seniority"]

        # Blocks
        if "context_block" in data:
            updates["context_block"] = data["context_block"]
        if "role_blocks" in data:
            updates["role_blocks"] = data["role_blocks"]
        if "goal_blocks" in data:
            updates["goal_blocks"] = data["goal_blocks"]
        if "selected_role_block_ids" in data:
            updates["selected_role_block_ids"] = data["selected_role_block_ids"]
        if "selected_goal_block_ids" in data:
            updates["selected_goal_block_ids"] = data["selected_goal_block_ids"]

        # Use cases
        if "generated_use_cases" in data:
            updates["generated_use_cases"] = data["generated_use_cases"]
        if "selected_use_cases" in data:
            updates["selected_use_cases"] = data["selected_use_cases"]

        # Additional data
        if "ai_dreams" in data:
            updates["ai_dreams"] = data["ai_dreams"]
        if "signup_source" in data:
            updates["signup_source"] = data["signup_source"]
        if "chat_history" in data:
            updates["chat_history"] = data["chat_history"]
        if "chat_summary" in data:
            updates["chat_summary"] = data["chat_summary"]

        return OnboardingRepository.update(client, user_id, updates)

    @staticmethod
    def set_extension_installed(
        client: Client,
        user_id: str,
        installed: bool = True,
    ) -> UserOnboarding:
        """
        Mark extension as installed/uninstalled.

        Args:
            client: Supabase client
            user_id: User's UUID
            installed: Whether extension is installed

        Returns:
            Updated UserOnboarding entity
        """
        return OnboardingRepository.update(
            client,
            user_id,
            {"extension_installed": installed},
        )

    @staticmethod
    def complete(client: Client, user_id: str) -> UserOnboarding:
        """
        Mark onboarding as completed.

        Args:
            client: Supabase client
            user_id: User's UUID

        Returns:
            Updated UserOnboarding entity
        """
        return OnboardingRepository.update_step(client, user_id, "completed")

    @staticmethod
    def _map_to_entity(data: dict[str, Any]) -> UserOnboarding:
        """
        Map database row to entity.

        Args:
            data: Database row dictionary

        Returns:
            UserOnboarding entity
        """
        # Parse context block
        context_block = None
        if data.get("context_block"):
            ctx = data["context_block"]
            if isinstance(ctx, str):
                ctx = json.loads(ctx)
            context_block = OnboardingBlock.from_dict(ctx)

        # Parse role blocks
        role_blocks = []
        if data.get("role_blocks"):
            blocks_data = data["role_blocks"]
            if isinstance(blocks_data, str):
                blocks_data = json.loads(blocks_data)
            role_blocks = [OnboardingBlock.from_dict(b) for b in blocks_data]

        # Parse goal blocks
        goal_blocks = []
        if data.get("goal_blocks"):
            blocks_data = data["goal_blocks"]
            if isinstance(blocks_data, str):
                blocks_data = json.loads(blocks_data)
            goal_blocks = [OnboardingBlock.from_dict(b) for b in blocks_data]

        # Parse use cases
        use_cases = []
        if data.get("generated_use_cases"):
            uc_data = data["generated_use_cases"]
            if isinstance(uc_data, str):
                uc_data = json.loads(uc_data)
            use_cases = [UseCase.from_dict(uc) for uc in uc_data]

        # Parse chat history
        chat_history = data.get("chat_history")
        if isinstance(chat_history, str):
            chat_history = json.loads(chat_history)

        # Parse timestamps
        completed_at = None
        if data.get("completed_at"):
            if isinstance(data["completed_at"], str):
                completed_at = datetime.fromisoformat(
                    data["completed_at"].replace("Z", "+00:00")
                )
            else:
                completed_at = data["completed_at"]

        dismissed_at = None
        if data.get("dismissed_at"):
            if isinstance(data["dismissed_at"], str):
                dismissed_at = datetime.fromisoformat(
                    data["dismissed_at"].replace("Z", "+00:00")
                )
            else:
                dismissed_at = data["dismissed_at"]

        created_at = None
        if data.get("created_at"):
            if isinstance(data["created_at"], str):
                created_at = datetime.fromisoformat(
                    data["created_at"].replace("Z", "+00:00")
                )
            else:
                created_at = data["created_at"]

        updated_at = None
        if data.get("updated_at"):
            if isinstance(data["updated_at"], str):
                updated_at = datetime.fromisoformat(
                    data["updated_at"].replace("Z", "+00:00")
                )
            else:
                updated_at = data["updated_at"]

        return UserOnboarding(
            id=data.get("id"),
            user_id=data.get("user_id", ""),
            flow_type=data.get("flow_type"),
            current_step=data.get("current_step", "not_started"),
            completed_at=completed_at,
            dismissed_at=dismissed_at,
            organization_name=data.get("organization_name"),
            organization_description=data.get("organization_description"),
            organization_logo_url=data.get("organization_logo_url"),
            industry=data.get("industry"),
            job_title=data.get("job_title"),
            job_description=data.get("job_description"),
            job_seniority=data.get("job_seniority"),
            context_block=context_block,
            role_blocks=role_blocks,
            goal_blocks=goal_blocks,
            selected_role_block_ids=data.get("selected_role_block_ids") or [],
            selected_goal_block_ids=data.get("selected_goal_block_ids") or [],
            generated_use_cases=use_cases,
            selected_use_cases=data.get("selected_use_cases") or [],
            ai_dreams=data.get("ai_dreams"),
            signup_source=data.get("signup_source"),
            chat_history=chat_history,
            chat_summary=data.get("chat_summary"),
            extension_installed=data.get("extension_installed", False),
            created_at=created_at,
            updated_at=updated_at,
        )


# Legacy compatibility - methods for user preferences in users_metadata table
# Note: onboarding_step, onboarding_flow_type, onboarding_completed_at are now in users_onboarding


class OnboardingRepositoryLegacy:
    """
    Legacy methods for backward compatibility with user preferences.

    These methods work with the users_metadata table for user settings
    like job_type, interests, etc. (NOT onboarding flow state).
    """

    @staticmethod
    def get_user_metadata(client: Client, user_id: str):
        """Get user preferences from users_metadata table."""
        from domains.entities.onboarding_entities import OnboardingStatus

        try:
            response = (
                client.table("users_metadata")
                .select(
                    "job_type, job_industry, job_seniority, interests, signup_source, "
                    "onboarding_dismissed, first_template_created, first_template_used, "
                    "first_block_created, keyboard_shortcut_used, extension_installed"
                )
                .eq("user_id", user_id)
                .maybe_single()
                .execute()
            )

            if response is None or not response.data:
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
                extension_installed=data.get("extension_installed", False),
            )
        except Exception as e:
            logger.warning(f"Could not fetch user metadata for {user_id}: {e}")
            return OnboardingStatus()

    @staticmethod
    def update_user_metadata(client: Client, user_id: str, metadata: dict) -> dict:
        """Update user preferences in users_metadata table."""
        try:
            existing = (
                client.table("users_metadata")
                .select("user_id")
                .eq("user_id", user_id)
                .maybe_single()
                .execute()
            )

            if existing and existing.data:
                response = (
                    client.table("users_metadata")
                    .update(metadata)
                    .eq("user_id", user_id)
                    .execute()
                )
            else:
                metadata["user_id"] = user_id
                response = client.table("users_metadata").insert(metadata).execute()

            if not response or not response.data:
                raise ValueError("Failed to update user metadata")

            return response.data[0]
        except Exception as e:
            logger.error(f"Error updating user metadata for {user_id}: {e}")
            raise
