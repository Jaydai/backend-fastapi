from supabase import Client
from dtos import (
    CreateFolderDTO,
    UpdateFolderDTO,
    FolderResponseDTO,
    FolderWithItemsDTO,
    UpdatePinnedFoldersDTO,
    FolderTitleResponseDTO,
)
from repositories.folder_repository import (
    get_folder_by_id as repo_get_folder_by_id,
    get_folders_titles as repo_get_folders_titles,
    create_folder as repo_create_folder,
    update_folder as repo_update_folder,
    delete_folder as repo_delete_folder,
    get_pinned_folder_ids,
    pin_folder as repo_pin_folder,
    unpin_folder as repo_unpin_folder,
    update_pinned_folders as repo_update_pinned_folders,
)
from mappers.folder_mapper import FolderMapper
from utils import localize_object


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
        # SECURITY FIX: Always pass user_id to repository for proper filtering
        # RLS policies at database level provide additional security layer
        filter_user_id = user_id
        filter_org_id = organization_id
        filter_parent_id = parent_folder_id

        folders = repo_get_folders_titles(
            client,
            user_id=filter_user_id,
            organization_id=filter_org_id,
            parent_folder_id=filter_parent_id,
            limit=limit,
            offset=offset
        )

        return [
            FolderTitleResponseDTO(**localize_object(folder.__dict__, locale, ["title"]))
            for folder in folders
        ]


    @staticmethod
    def get_folder_by_id(
        client: Client,
        folder_id: str,
        locale: str = "en"
    ) -> FolderResponseDTO | None:
        """Get folder by ID"""
        folder = repo_get_folder_by_id(client, folder_id)
        if not folder:
            return None
        return FolderMapper.entity_to_response_dto(folder, locale)

    @staticmethod
    def create_folder(
        client: Client,
        user_id: str,
        data: CreateFolderDTO,
        locale: str = "en"
    ) -> FolderResponseDTO:
        """Create a new folder"""
        workspace_type = "user"
        if data.organization_id:
            workspace_type = "organization"

        title_dict = FolderMapper.ensure_localized_dict(data.title, locale)
        description_dict = (
            FolderMapper.ensure_localized_dict(data.description, locale)
            if data.description else None
        )

        folder = repo_create_folder(
            client,
            user_id,
            title_dict,
            description_dict,
            data.parent_folder_id,
            data.organization_id,
            workspace_type
        )

        return FolderMapper.entity_to_response_dto(folder, locale)

    @staticmethod
    def update_folder(
        client: Client,
        folder_id: str,
        data: UpdateFolderDTO,
        locale: str = "en"
    ) -> FolderResponseDTO | None:
        """Update a folder"""
        title_dict = (
            FolderMapper.ensure_localized_dict(data.title, locale)
            if data.title else None
        )
        description_dict = (
            FolderMapper.ensure_localized_dict(data.description, locale)
            if data.description else None
        )

        folder = repo_update_folder(
            client,
            folder_id,
            title_dict,
            description_dict,
            data.parent_folder_id
        )

        if not folder:
            return None

        return FolderMapper.entity_to_response_dto(folder, locale)

    @staticmethod
    def delete_folder(client: Client, folder_id: str) -> bool:
        """Delete a folder"""
        return repo_delete_folder(client, folder_id)

    @staticmethod
    def get_pinned_folders(
        client: Client,
        user_id: str,
        locale: str = "en"
    ) -> list[FolderResponseDTO]:
        """Get pinned folders"""
        pinned_ids = get_pinned_folder_ids(client, user_id)

        if not pinned_ids:
            return []

        folders = []
        for folder_id in pinned_ids:
            folder = repo_get_folder_by_id(client, folder_id)
            if folder:
                folders.append(folder)

        return [FolderMapper.entity_to_response_dto(f, locale) for f in folders]

    @staticmethod
    def pin_folder(client: Client, user_id: str, folder_id: str) -> dict:
        """Pin a folder"""
        pinned_ids = repo_pin_folder(client, user_id, folder_id)
        return {"pinned": True, "pinned_folder_ids": pinned_ids}

    @staticmethod
    def unpin_folder(client: Client, user_id: str, folder_id: str) -> dict:
        """Unpin a folder"""
        pinned_ids = repo_unpin_folder(client, user_id, folder_id)
        return {"pinned": False, "pinned_folder_ids": pinned_ids}

    @staticmethod
    def update_pinned_folders(
        client: Client,
        user_id: str,
        data: UpdatePinnedFoldersDTO
    ) -> dict:
        """Update pinned folders"""
        pinned_ids = repo_update_pinned_folders(client, user_id, data.folder_ids)
        return {"pinned_folder_ids": pinned_ids}

    @staticmethod
    def get_root_items(
        client: Client,
        user_id: str,
        locale: str = "en",
        workspace_type: str | None = None,
        organization_id: str | None = None
    ) -> FolderWithItemsDTO:
        """Get root items"""
        raise NotImplementedError("get_root_items is not implemented in FolderService yet.")

    @staticmethod
    def get_folder_items(
        client: Client,
        folder_id: str,
        locale: str = "en",
        limit: int | None = None,
        offset: int = 0
    ) -> FolderWithItemsDTO:
        """Get folder items"""
        raise NotImplementedError("get_folder_items is not implemented in FolderService yet.")
