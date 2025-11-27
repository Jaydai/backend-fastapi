"""Get folder titles service"""
from supabase import Client
from dtos import FolderTitleResponseDTO
from repositories.folders import get_folders_titles as repo_get_folders_titles
from services.locale_service import LocaleService
from utils import localize_object


def get_folders_titles(
    client: Client,
    locale: str = LocaleService.DEFAULT_LOCALE,
    user_id: str | None = None,
    organization_id: str | None = None,
    parent_folder_id: str | None = None,
    published: bool | None = None,
    limit: int = 100,
    offset: int = 0
) -> list[FolderTitleResponseDTO]:

    # Business logic: Determine which filters to apply based on priority
    filter_user_id = None
    filter_org_id = None
    filter_parent_id = parent_folder_id
    if parent_folder_id is not None:
        # Priority 1: Filter by parent folder only
        pass
    elif organization_id:
        # Priority 2: Filter by organization only
        filter_org_id = organization_id
    elif user_id:
        # Priority 3: Filter by user only
        filter_user_id = user_id
    # Priority 4: No filters (RLS handles access)

    folders = repo_get_folders_titles(
        client,
        user_id=filter_user_id,
        organization_id=filter_org_id,
        parent_folder_id=filter_parent_id,
        published=published,
        limit=limit,
        offset=offset
    )

    return [
        FolderTitleResponseDTO(**localize_object(folder.__dict__, locale, ["title"]))
        for folder in folders
    ]
