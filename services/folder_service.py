from supabase import Client
from dtos import (
    CreateFolderDTO,
    UpdateFolderDTO,
    FolderResponseDTO,
    FolderWithItemsDTO,
    UpdatePinnedFoldersDTO,
    FolderTitleResponseDTO,
)
from services.folders import (
    get_folder_by_id,
    create_folder,
    update_folder,
    delete_folder,
    get_pinned_folders,
    pin_folder,
    unpin_folder,
    update_pinned_folders,
)
from repositories.folder_repository import FolderRepository
from mappers.folder_mapper import FolderMapper
from services.locale_service import LocaleService
from repositories import FolderRepository


class FolderService:
    """Folder service class for backward compatibility"""

    @staticmethod
    def get_folders_titles(
        client: Client,
        user_id: str,
        locale: str = LocaleService.DEFAULT_LOCALE,
        organization_id: str | None = None,
        parent_folder_id: str | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[FolderTitleResponseDTO]:
        """Get folder titles with optional filtering"""
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

        folders = FolderRepository.get_folders_titles(
            client,
            user_id=filter_user_id,
            organization_id=filter_org_id,
            parent_folder_id=filter_parent_id,
            limit=limit,
            offset=offset
        )

        return [
            FolderTitleResponseDTO(**LocaleService.localize_object(folder.__dict__, locale, ["title"]))
            for folder in folders
        ]

    @staticmethod
    def get_folder_by_id(
        client: Client,
        folder_id: str,
        locale: str = LocaleService.DEFAULT_LOCALE
    ) -> FolderResponseDTO | None:
        """Get folder by ID"""
        return get_folder_by_id(client, folder_id, locale)

    @staticmethod
    def create_folder(
        client: Client,
        user_id: str,
        data: CreateFolderDTO,
        locale: str = LocaleService.DEFAULT_LOCALE
    ) -> FolderResponseDTO:
        """Create a new folder"""
        return create_folder(client, user_id, data, locale)

    @staticmethod
    def update_folder(
        client: Client,
        folder_id: str,
        data: UpdateFolderDTO,
        locale: str = LocaleService.DEFAULT_LOCALE
    ) -> FolderResponseDTO | None:
        """Update a folder"""
        return update_folder(client, folder_id, data, locale)

    @staticmethod
    def delete_folder(client: Client, folder_id: str) -> bool:
        """Delete a folder"""
        return delete_folder(client, folder_id)

    @staticmethod
    def get_pinned_folders(
        client: Client,
        user_id: str,
        locale: str = LocaleService.DEFAULT_LOCALE
    ) -> list[FolderResponseDTO]:
        """Get pinned folders"""
        return get_pinned_folders(client, user_id, locale)

    @staticmethod
    def pin_folder(client: Client, user_id: str, folder_id: str) -> dict:
        """Pin a folder"""
        return pin_folder(client, user_id, folder_id)

    @staticmethod
    def unpin_folder(client: Client, user_id: str, folder_id: str) -> dict:
        """Unpin a folder"""
        return unpin_folder(client, user_id, folder_id)

    @staticmethod
    def update_pinned_folders(
        client: Client,
        user_id: str,
        data: UpdatePinnedFoldersDTO
    ) -> dict:
        """Update pinned folders"""
        return update_pinned_folders(client, user_id, data)
