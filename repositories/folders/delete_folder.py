"""Delete folder"""

from supabase import Client


def delete_folder(client: Client, folder_id: str) -> bool:
    """Delete a folder by ID"""
    response = client.table("prompt_folders").delete().eq("id", folder_id).execute()
    return len(response.data or []) > 0
