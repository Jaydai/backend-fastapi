"""Get folder titles repository"""

from domains.entities import FolderTitle
from supabase import Client


def get_folders_titles(
    client: Client,
    user_id: str | None = None,
    organization_id: str | None = None,
    published: bool | None = None,
    parent_folder_id: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[FolderTitle]:
    """
    Repository function to fetch folder titles from database.
    Applies filters as provided by the service layer.
    """
    query = client.table("prompt_folders").select("id, title, parent_folder_id")

    # Apply filters as provided
    if user_id:
        query = query.eq("user_id", user_id)

    if organization_id:
        query = query.eq("organization_id", organization_id)

    # Don't filter by parent_folder_id - we want ALL folders for tree building
    # The tree building happens client-side using parent_folder_id field
    if published is not None:
        query = query.eq("published", published)
    query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
    response = query.execute()
    folders_data = response.data or []

    folders = [FolderTitle(**item) for item in folders_data]
    return folders
