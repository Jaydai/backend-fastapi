"""Get folder by ID"""
from supabase import Client
from domains.entities import Folder


def get_folder_by_id(client: Client, folder_id: str) -> Folder | None:
    """Get a single folder by ID"""
    response = client.table("prompt_folders")\
        .select("*")\
        .eq("id", folder_id)\
        .execute()

    if not response.data:
        return None

    data = response.data[0]
    return Folder(
        id=data["id"],
        title=data.get("title", {}),
        description=data.get("description"),
        user_id=data.get("user_id"),
        organization_id=data.get("organization_id"),
        parent_folder_id=data.get("parent_folder_id"),
        workspace_type=data["workspace_type"],
        created_at=data["created_at"],
        updated_at=data.get("updated_at")
    )
