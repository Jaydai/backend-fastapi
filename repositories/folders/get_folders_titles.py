"""Get folder titles - simplified version"""
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
    Get folder titles (id, title) with simple filtering.

    Logic:
    - If parent_folder_id provided: Get folders in that parent folder
    - Else if organization_id provided: Get folders for that organization
    - Else if user_id provided: Get folders for that user
    - Else: Get all folders (RLS will filter based on access)
    """
    query = client.table("prompt_folders").select("id, title")

    # Priority 1: Filter by parent folder if specified
    if parent_folder_id is not None:
        if parent_folder_id == "root" or parent_folder_id == "":
            query = query.is_("parent_folder_id", "null")
        else:
            query = query.eq("parent_folder_id", parent_folder_id)
    # Priority 2: Filter by organization
    elif organization_id:
        query = query.eq("organization_id", organization_id)
    # Priority 3: Filter by user
    elif user_id:
        query = query.eq("user_id", user_id)
    # Priority 4: Get all (RLS will filter)

    query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
    response = query.execute()
    folders_data = response.data or []

    folders = [FolderTitle(**item) for item in folders_data]
    return folders