"""Create folder service"""
from supabase import Client
from dtos import CreateFolderDTO, FolderResponseDTO
from repositories.folders import create_folder as repo_create_folder
from mappers.folder_mapper import FolderMapper


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
    description_dict = FolderMapper.ensure_localized_dict(data.description, locale) if data.description else None

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
