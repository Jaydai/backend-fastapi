"""Update folder service"""
from supabase import Client
from dtos import UpdateFolderDTO, FolderResponseDTO
from repositories.folders import update_folder as repo_update_folder
from mappers.folder_mapper import FolderMapper
from services.locale_service import LocaleService


def update_folder(
    client: Client,
    folder_id: str,
    data: UpdateFolderDTO,
    locale: str = LocaleService.DEFAULT_LOCALE
) -> FolderResponseDTO | None:
    """Update an existing folder"""
    title_dict = LocaleService.ensure_localized_dict(data.title, locale) if data.title else None
    description_dict = LocaleService.ensure_localized_dict(data.description, locale) if data.description else None

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
