"""Pinned folders operations"""
from supabase import Client


def get_pinned_folder_ids(client: Client, user_id: str) -> list[str]:
    """Get list of pinned folder IDs for a user"""
    response = client.table("users_metadata")\
        .select("pinned_folder_ids")\
        .eq("user_id", user_id)\
        .single()\
        .execute()

    if not response.data:
        return []

    pinned_ids = response.data.get("pinned_folder_ids") or []
    return [str(fid) for fid in pinned_ids]


def pin_folder(client: Client, user_id: str, folder_id: str) -> list[str]:
    """Pin a folder for a user"""
    current_pinned = get_pinned_folder_ids(client, user_id)

    if folder_id not in current_pinned:
        current_pinned.append(folder_id)

    client.table("users_metadata")\
        .update({"pinned_folder_ids": current_pinned})\
        .eq("user_id", user_id)\
        .execute()

    return current_pinned


def unpin_folder(client: Client, user_id: str, folder_id: str) -> list[str]:
    """Unpin a folder for a user"""
    current_pinned = get_pinned_folder_ids(client, user_id)

    if folder_id in current_pinned:
        current_pinned.remove(folder_id)

    client.table("users_metadata")\
        .update({"pinned_folder_ids": current_pinned})\
        .eq("user_id", user_id)\
        .execute()

    return current_pinned


def update_pinned_folders(client: Client, user_id: str, folder_ids: list[str]) -> list[str]:
    """Update all pinned folders for a user"""
    client.table("users_metadata")\
        .update({"pinned_folder_ids": folder_ids})\
        .eq("user_id", user_id)\
        .execute()

    return folder_ids
