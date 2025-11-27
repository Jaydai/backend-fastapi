"""Block title service - handles business logic for block list operations"""
from supabase import Client
from dtos import BlockTitleResponseDTO
from repositories.blocks import BlockBaseRepository
from services.permissions import UserPermissionsService
from services.locale_service import LocaleService

class BlockTitleService:
    """Service for block title operations (list views)"""

    @staticmethod
    def get_titles(
        client: Client,
        locale: str = LocaleService.DEFAULT_LOCALE,
        organization_id: str | None = None,
        types: list[str] | None = None,
        published: bool | None = None,
        user_id: str | None = None,
        workspace_type: str | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[BlockTitleResponseDTO]:
        """
        Get block titles with optional filtering and permission checks.
        """
        # Build permission filter if user_id and workspace_type provided
        or_conditions = None
        if user_id and workspace_type:
            filter_result = UserPermissionsService.build_workspace_filter_conditions(
                client, user_id, workspace_type, organization_id
            )

            if filter_result["type"] == "none":
                return []
            elif filter_result["type"] == "or":
                or_conditions = filter_result["conditions"]
                organization_id = None
            elif filter_result["type"] == "organization":
                organization_id = filter_result["org_id"]
            elif filter_result["type"] == "organizations":
                or_conditions = [f"organization_id.eq.{org_id}" for org_id in filter_result["org_ids"]]
                organization_id = None
            elif filter_result["type"] == "user":
                user_id = user_id
                organization_id = None

        # Fetch from repository
        blocks = BlockBaseRepository.get_blocks_titles(
            client,
            organization_id=organization_id,
            types=types,
            published=published,
            user_id=user_id if not or_conditions else None,
            or_conditions=or_conditions,
            limit=limit,
            offset=offset
        )

        # Localize and convert to DTOs
        return [
            BlockTitleResponseDTO(**LocaleService.localize_object(block.__dict__, locale, ["title"]))
            for block in blocks
        ]
