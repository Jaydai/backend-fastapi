"""Pinned folders service"""
from supabase import Client
from dtos import FolderResponseDTO, UpdatePinnedFoldersDTO
from repositories.folders import (
    get_pinned_folder_ids,
    get_folder_by_id,
    pin_folder as repo_pin_folder,
    unpin_folder as repo_unpin_folder,
    update_pinned_folders as repo_update_pinned_folders
)
from mappers.folder_mapper import FolderMapper


def get_pinned_folders(
    client: Client,
    user_id: str,
    locale: str = "en"
) -> list[FolderResponseDTO]:
    """Get all pinned folders for a user"""
    pinned_ids = get_pinned_folder_ids(client, user_id)

    if not pinned_ids:
        return []

    folders = []
    for folder_id in pinned_ids:
        folder = get_folder_by_id(client, folder_id)
        if folder:
            folders.append(folder)

    return [FolderMapper.entity_to_response_dto(f, locale) for f in folders]


def pin_folder(client: Client, user_id: str, folder_id: str) -> dict:
    """Pin a folder"""
    pinned_ids = repo_pin_folder(client, user_id, folder_id)
    return {"pinned": True, "pinned_folder_ids": pinned_ids}


def unpin_folder(client: Client, user_id: str, folder_id: str) -> dict:
    """Unpin a folder"""
    pinned_ids = repo_unpin_folder(client, user_id, folder_id)
    return {"pinned": False, "pinned_folder_ids": pinned_ids}


def update_pinned_folders(
    client: Client,
    user_id: str,
    data: UpdatePinnedFoldersDTO
) -> dict:
    """Update all pinned folders"""
    pinned_ids = repo_update_pinned_folders(client, user_id, data.folder_ids)
    return {"pinned_folder_ids": pinned_ids}
