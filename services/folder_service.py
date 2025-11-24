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
    get_folders_titles,
    create_folder,
    update_folder,
    delete_folder,
    get_pinned_folders,
    pin_folder,
    unpin_folder,
    update_pinned_folders,
)


class FolderService:
    """Folder service class for backward compatibility"""

    @staticmethod
    def get_folders_titles(
        client: Client,
        locale: str = "en",
        user_id: str | None = None,
        organization_id: str | None = None,
        parent_folder_id: str | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[FolderTitleResponseDTO]:
        """Get folder titles with optional filtering"""
        return get_folders_titles(
            client=client,
            locale=locale,
            user_id=user_id,
            organization_id=organization_id,
            parent_folder_id=parent_folder_id,
            limit=limit,
            offset=offset
        )


    @staticmethod
    def get_folder_by_id(
        client: Client,
        folder_id: str,
        locale: str = "en"
    ) -> FolderResponseDTO | None:
        """Get folder by ID"""
        return get_folder_by_id(client, folder_id, locale)

    @staticmethod
    def create_folder(
        client: Client,
        user_id: str,
        data: CreateFolderDTO,
        locale: str = "en"
    ) -> FolderResponseDTO:
        """Create a new folder"""
        return create_folder(client, user_id, data, locale)

    @staticmethod
    def update_folder(
        client: Client,
        folder_id: str,
        data: UpdateFolderDTO,
        locale: str = "en"
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
        locale: str = "en"
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

    @staticmethod
    def get_root_items(
        client: Client,
        user_id: str,
        locale: str = "en",
        workspace_type: str | None = None,
        organization_id: str | None = None
    ) -> FolderWithItemsDTO:
        """Get root items"""
        return get_root_items(client, user_id, locale, workspace_type, organization_id)

    @staticmethod
    def get_folder_items(
        client: Client,
        folder_id: str,
        locale: str = "en",
        limit: int | None = None,
        offset: int = 0
    ) -> FolderWithItemsDTO:
        """Get folder items"""
        return get_folder_items(client, folder_id, locale, limit, offset)