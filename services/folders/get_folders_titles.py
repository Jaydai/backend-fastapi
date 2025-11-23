"""Get folder titles service"""
from supabase import Client
from dtos import FolderTitleResponseDTO
from repositories.folders import get_folders_titles as repo_get_folders_titles
from utils import localize_object


def get_folders_titles(
    client: Client,
    locale: str = "en",
    user_id: str | None = None,
    organization_id: str | None = None,
    parent_folder_id: str | None = None,
    limit: int = 100,
    offset: int = 0
) -> list[FolderTitleResponseDTO]:
    """
    Get folder titles with localization.

    Args:
        client: Supabase client
        locale: Locale for localization
        user_id: Filter by user ID
        organization_id: Filter by organization ID
        parent_folder_id: Filter by parent folder ID (overrides user/org)
        limit: Max results
        offset: Pagination offset

    Returns:
        List of localized folder title DTOs
    """
    folders = repo_get_folders_titles(
        client,
        user_id=user_id,
        organization_id=organization_id,
        parent_folder_id=parent_folder_id,
        limit=limit,
        offset=offset
    )

    return [
        FolderTitleResponseDTO(**localize_object(folder.__dict__, locale, ["title"]))
        for folder in folders
    ]
