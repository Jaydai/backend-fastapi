"""
Folder Repository helpers and backward-compatible class wrapper.
"""

from __future__ import annotations

from typing import Optional

from supabase import Client

from domains.entities import Folder, FolderTitle


def _row_to_folder(row: dict) -> Folder:
    return Folder(
        id=row["id"],
        title=row.get("title", {}),
        description=row.get("description"),
        user_id=row.get("user_id"),
        organization_id=row.get("organization_id"),
        parent_folder_id=row.get("parent_folder_id"),
        workspace_type=row["workspace_type"],
        created_at=row["created_at"],
        updated_at=row.get("updated_at"),
    )


def get_folders_titles(
    client: Client,
    user_id: str | None = None,
    organization_id: str | None = None,
    parent_folder_id: str | None = None,
    published: bool | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[FolderTitle]:
    query = client.table("prompt_folders").select("id, title, parent_folder_id")

    if user_id:
        query = query.eq("user_id", user_id)
    if organization_id:
        query = query.eq("organization_id", organization_id)

    if parent_folder_id == "ROOT":
        query = query.is_("parent_folder_id", "null")
    elif parent_folder_id is not None:
        query = query.eq("parent_folder_id", parent_folder_id)

    if published is not None:
        query = query.eq("published", published)

    response = query.order("created_at", desc=True).range(offset, offset + limit - 1).execute()
    return [FolderTitle(**item) for item in (response.data or [])]


def get_folder_by_id(client: Client, folder_id: str) -> Folder | None:
    response = (
        client.table("prompt_folders")
        .select("*")
        .eq("id", folder_id)
        .execute()
    )
    if not response.data:
        return None
    return _row_to_folder(response.data[0])


def create_folder(
    client: Client,
    user_id: str,
    title: dict[str, str],
    description: dict[str, str] | None,
    parent_folder_id: str | None,
    organization_id: str | None,
    workspace_type: str,
) -> Folder:
    payload = {
        "user_id": user_id,
        "title": title,
        "description": description,
        "parent_folder_id": parent_folder_id,
        "organization_id": organization_id,
        "workspace_type": workspace_type,
    }
    response = client.table("prompt_folders").insert(payload).execute()
    return _row_to_folder(response.data[0])


def update_folder(
    client: Client,
    folder_id: str,
    title: dict[str, str] | None = None,
    description: dict[str, str] | None = None,
    parent_folder_id: str | None = None,
) -> Folder | None:
    update_data: dict[str, object] = {}
    if title is not None:
        update_data["title"] = title
    if description is not None:
        update_data["description"] = description
    if parent_folder_id is not None:
        update_data["parent_folder_id"] = parent_folder_id

    if not update_data:
        return get_folder_by_id(client, folder_id)

    response = (
        client.table("prompt_folders")
        .update(update_data)
        .eq("id", folder_id)
        .execute()
    )
    if not response.data:
        return None
    return _row_to_folder(response.data[0])


def delete_folder(client: Client, folder_id: str) -> bool:
    response = client.table("prompt_folders").delete().eq("id", folder_id).execute()
    return bool(response.data)


def get_pinned_folder_ids(client: Client, user_id: str) -> list[str]:
    response = (
        client.table("users_metadata")
        .select("pinned_folder_ids")
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    if not response.data:
        return []
    return [str(fid) for fid in (response.data.get("pinned_folder_ids") or [])]


def pin_folder(client: Client, user_id: str, folder_id: str) -> list[str]:
    pinned = get_pinned_folder_ids(client, user_id)
    if folder_id not in pinned:
        pinned.append(folder_id)
        (
            client.table("users_metadata")
            .update({"pinned_folder_ids": pinned})
            .eq("user_id", user_id)
            .execute()
        )
    return pinned


def unpin_folder(client: Client, user_id: str, folder_id: str) -> list[str]:
    pinned = get_pinned_folder_ids(client, user_id)
    if folder_id in pinned:
        pinned.remove(folder_id)
        (
            client.table("users_metadata")
            .update({"pinned_folder_ids": pinned})
            .eq("user_id", user_id)
            .execute()
        )
    return pinned


def update_pinned_folders(client: Client, user_id: str, folder_ids: list[str]) -> list[str]:
    (
        client.table("users_metadata")
        .update({"pinned_folder_ids": folder_ids})
        .eq("user_id", user_id)
        .execute()
    )
    return folder_ids


class FolderRepository:
    """Backward-compatible class wrapper for legacy imports."""

    @staticmethod
    def get_folders_titles(client, user_id=None, organization_id=None, parent_folder_id=None, limit=100, offset=0):
        return get_folders_titles(
            client,
            user_id=user_id,
            organization_id=organization_id,
            parent_folder_id=parent_folder_id,
            limit=limit,
            offset=offset,
        )

    @staticmethod
    def get_folder_by_id(client, folder_id: str):
        return get_folder_by_id(client, folder_id)

    @staticmethod
    def create_folder(client, user_id: str, title, description, parent_folder_id, organization_id, workspace_type):
        return create_folder(client, user_id, title, description, parent_folder_id, organization_id, workspace_type)

    @staticmethod
    def update_folder(client, folder_id: str, title=None, description=None, parent_folder_id=None):
        return update_folder(client, folder_id, title, description, parent_folder_id)

    @staticmethod
    def delete_folder(client, folder_id: str) -> bool:
        return delete_folder(client, folder_id)

    @staticmethod
    def get_pinned_folder_ids(client, user_id: str):
        return get_pinned_folder_ids(client, user_id)

    @staticmethod
    def pin_folder(client, user_id: str, folder_id: str):
        return pin_folder(client, user_id, folder_id)

    @staticmethod
    def unpin_folder(client, user_id: str, folder_id: str):
        return unpin_folder(client, user_id, folder_id)

    @staticmethod
    def update_pinned_folders(client, user_id: str, folder_ids):
        return update_pinned_folders(client, user_id, folder_ids)
