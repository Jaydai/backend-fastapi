"""Get folder titles repository"""
from supabase import Client
from domains.entities import FolderTitle


def get_folders_titles(
    client: Client,
    user_id: str | None = None,
    organization_id: str | None = None,
    parent_folder_id: str | None = None,
    limit: int = 100,
    offset: int = 0
) -> list[FolderTitle]:
    """
    Repository function to fetch folder titles from database.
    Applies filters as provided by the service layer.
    """
    query = client.table("prompt_folders").select("id, title")

    # Apply filters as provided
    if user_id:
        query = query.eq("user_id", user_id)

    if organization_id:
        query = query.eq("organization_id", organization_id)

    if parent_folder_id is not None:
        query = query.eq("parent_folder_id", parent_folder_id)
    else:
        query = query.is_("parent_folder_id", "null")

    query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
    response = query.execute()
    folders_data = response.data or []

    folders = [FolderTitle(**item) for item in folders_data]
    return folders