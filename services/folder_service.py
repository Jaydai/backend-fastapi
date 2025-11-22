from supabase import Client
from dtos import (
    CreateFolderDTO,
    UpdateFolderDTO,
    FolderResponseDTO,
    FolderWithItemsDTO,
    UpdatePinnedFoldersDTO,
    OrganizationFolderTitleDTO
)
from repositories.folder_repository import FolderRepository
from mappers.folder_mapper import FolderMapper

class FolderService:
    @staticmethod
    def get_folders(
        client: Client,
        user_id: str,
        locale: str = "en",
        workspace_type: str | None = None,
        organization_id: str | None = None,
        parent_folder_id: str | None = None
    ) -> list[FolderResponseDTO]:
        folders = FolderRepository.get_folders(
            client,
            user_id,
            workspace_type,
            organization_id,
            parent_folder_id
        )

        return [FolderMapper.entity_to_response_dto(f, locale) for f in folders]

    @staticmethod
    def get_folder_by_id(
        client: Client,
        folder_id: str,
        locale: str = "en"
    ) -> FolderResponseDTO | None:
        folder = FolderRepository.get_folder_by_id(client, folder_id)
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
        workspace_type = "user"
        if data.organization_id:
            workspace_type = "organization"

        title_dict = FolderMapper.ensure_localized_dict(data.title, locale)
        description_dict = FolderMapper.ensure_localized_dict(data.description, locale) if data.description else None

        folder = FolderRepository.create_folder(
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
        title_dict = FolderMapper.ensure_localized_dict(data.title, locale) if data.title else None
        description_dict = FolderMapper.ensure_localized_dict(data.description, locale) if data.description else None

        folder = FolderRepository.update_folder(
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
        return FolderRepository.delete_folder(client, folder_id)

    @staticmethod
    def get_pinned_folders(
        client: Client,
        user_id: str,
        locale: str = "en"
    ) -> list[FolderResponseDTO]:
        pinned_ids = FolderRepository.get_pinned_folder_ids(client, user_id)

        if not pinned_ids:
            return []

        folders = []
        for folder_id in pinned_ids:
            folder = FolderRepository.get_folder_by_id(client, folder_id)
            if folder:
                folders.append(folder)

        return [FolderMapper.entity_to_response_dto(f, locale) for f in folders]

    @staticmethod
    def pin_folder(client: Client, user_id: str, folder_id: str) -> dict:
        pinned_ids = FolderRepository.pin_folder(client, user_id, folder_id)
        return {"pinned": True, "pinned_folder_ids": pinned_ids}

    @staticmethod
    def unpin_folder(client: Client, user_id: str, folder_id: str) -> dict:
        pinned_ids = FolderRepository.unpin_folder(client, user_id, folder_id)
        return {"pinned": False, "pinned_folder_ids": pinned_ids}

    @staticmethod
    def update_pinned_folders(
        client: Client,
        user_id: str,
        data: UpdatePinnedFoldersDTO
    ) -> dict:
        pinned_ids = FolderRepository.update_pinned_folders(client, user_id, data.folder_ids)
        return {"pinned_folder_ids": pinned_ids}

    @staticmethod
    def get_root_items(
        client: Client,
        user_id: str,
        locale: str = "en",
        workspace_type: str | None = None,
        organization_id: str | None = None
    ) -> FolderWithItemsDTO:
        items = FolderRepository.get_root_items(
            client,
            user_id,
            workspace_type,
            organization_id
        )

        return FolderMapper.folder_with_items_to_dto(
            items["folders"],
            items["templates"],
            locale
        )

    @staticmethod
    def get_folder_items(
        client: Client,
        folder_id: str,
        locale: str = "en",
        limit: int | None = None,
        offset: int = 0
    ) -> FolderWithItemsDTO:
        # Check if folder exists
        folder = FolderRepository.get_folder_by_id(client, folder_id)
        if not folder:
            raise ValueError(f"Folder not found: {folder_id}")

        items = FolderRepository.get_folder_items(client, folder_id, limit, offset)

        return FolderMapper.folder_with_items_to_dto(
            items["folders"],
            items["templates"],
            locale,
            items.get("total_count", 0),
            items.get("has_more", False)
        )

    @staticmethod
    def get_organization_folder_titles(
        client: Client,
        organization_id: str,
        locale: str = "en"
    ) -> list[OrganizationFolderTitleDTO]:
        """
        Get folder titles for a specific organization (localized).
        """
        from utils import localize_object

        folders_data = FolderRepository.get_organization_folder_titles(client, organization_id)

        result = []
        for folder_data in folders_data:
            # Localize the title
            localized = localize_object(folder_data, locale, ["title"])
            result.append(OrganizationFolderTitleDTO(
                id=localized["id"],
                title=localized["title"]
            ))

        return result
