"""Delete folder service"""
from supabase import Client
from repositories.folders import delete_folder as repo_delete_folder


def delete_folder(client: Client, folder_id: str) -> bool:
    """Delete a folder"""
    return repo_delete_folder(client, folder_id)
