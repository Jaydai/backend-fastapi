"""Create folder"""
from supabase import Client
from domains.entities import Folder


def create_folder(
    client: Client,
    user_id: str,
    title: dict[str, str],
    description: dict[str, str] | None,
    parent_folder_id: str | None,
    organization_id: str | None,
    workspace_type: str
) -> Folder:
    """Create a new folder"""
    folder_data = {
        "user_id": user_id,
        "title": title,
        "description": description,
        "parent_folder_id": parent_folder_id,
        "organization_id": organization_id,
        "workspace_type": workspace_type
    }

    response = client.table("prompt_folders").insert(folder_data).execute()

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
