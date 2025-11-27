"""Get folder by ID service"""
from supabase import Client
from dtos import FolderResponseDTO
from repositories.folders import get_folder_by_id as repo_get_folder_by_id
from mappers.folder_mapper import FolderMapper
from services.locale_service import LocaleService


def get_folder_by_id(
    client: Client,
    folder_id: str,
    locale: str = LocaleService.DEFAULT_LOCALE
) -> FolderResponseDTO | None:
    """Get a single folder by ID"""
    folder = repo_get_folder_by_id(client, folder_id)
    if not folder:
        return None

    return FolderMapper.entity_to_response_dto(folder, locale)
