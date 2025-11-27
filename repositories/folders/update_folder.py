"""Update folder"""

from supabase import Client

from domains.entities import Folder


def update_folder(
    client: Client,
    folder_id: str,
    title: dict[str, str] | None = None,
    description: dict[str, str] | None = None,
    parent_folder_id: str | None = None,
) -> Folder | None:
    """Update an existing folder"""
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if description is not None:
        update_data["description"] = description
    if parent_folder_id is not None:
        update_data["parent_folder_id"] = parent_folder_id

    response = client.table("prompt_folders").update(update_data).eq("id", folder_id).execute()

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
        updated_at=data.get("updated_at"),
    )
