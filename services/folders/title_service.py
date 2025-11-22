"""Folder title service - handles business logic for folder list operations"""
from supabase import Client
from dtos import FolderTitleResponseDTO
from repositories.folders import FolderBaseRepository
from services.permissions import UserPermissionsService
from utils import localize_object

class FolderTitleService:
    """Service for folder title operations (list views)"""

    @staticmethod
    def get_titles(
        client: Client,
        locale: str = "en",
        organization_id: str | None = None,
        parent_folder_ids: list[str] | None = None,
        user_id: str | None = None,
        workspace_type: str | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[FolderTitleResponseDTO]:
        """
        Get folder titles with optional filtering and permission checks.
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
        folders = FolderBaseRepository.get_folders_titles(
            client,
            organization_id=organization_id,
            parent_folder_ids=parent_folder_ids,
            user_id=user_id if not or_conditions else None,
            or_conditions=or_conditions,
            limit=limit,
            offset=offset
        )

        # Localize and convert to DTOs
        return [
            FolderTitleResponseDTO(**localize_object(folder.__dict__, locale, ["title"]))
            for folder in folders
        ]
