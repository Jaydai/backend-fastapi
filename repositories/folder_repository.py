"""
Folder Repository - Backward compatibility wrapper

This file now re-exports functions from the folders/ subdirectory.
For new code, import directly from repositories.folders.* modules.
"""

from repositories.folders import (
    get_folder_by_id,
    get_folders_titles,
    create_folder,
    update_folder,
    delete_folder,
    get_pinned_folder_ids,
    pin_folder,
    unpin_folder,
    update_pinned_folders,
)


class FolderRepository:
    """Folder repository class for backward compatibility"""

    @staticmethod
    def get_folders_titles(client, user_id=None, organization_id=None, parent_folder_id=None, limit=100, offset=0):
        """Get folder titles"""
        return get_folders_titles(
            client,
            user_id=user_id,
            organization_id=organization_id,
            parent_folder_id=parent_folder_id,
            limit=limit,
            offset=offset
        )

    @staticmethod
    def get_folder_by_id(client, folder_id: str):
        """Get folder by ID"""
        return get_folder_by_id(client, folder_id)

    @staticmethod
    def create_folder(client, user_id: str, title, description, parent_folder_id, organization_id, workspace_type):
        """Create a new folder"""
        return create_folder(client, user_id, title, description, parent_folder_id, organization_id, workspace_type)

    @staticmethod
    def update_folder(client, folder_id: str, title=None, description=None, parent_folder_id=None):
        """Update folder"""
        return update_folder(client, folder_id, title, description, parent_folder_id)

    @staticmethod
    def delete_folder(client, folder_id: str) -> bool:
        """Delete folder"""
        return delete_folder(client, folder_id)

    @staticmethod
    def get_pinned_folder_ids(client, user_id: str):
        """Get pinned folder IDs"""
        return get_pinned_folder_ids(client, user_id)

    @staticmethod
    def pin_folder(client, user_id: str, folder_id: str):
        """Pin a folder"""
        return pin_folder(client, user_id, folder_id)

    @staticmethod
    def unpin_folder(client, user_id: str, folder_id: str):
        """Unpin a folder"""
        return unpin_folder(client, user_id, folder_id)

    @staticmethod
    def update_pinned_folders(client, user_id: str, folder_ids):
        """Update pinned folders"""
        return update_pinned_folders(client, user_id, folder_ids)