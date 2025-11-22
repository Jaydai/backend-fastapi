"""Folder repository - handles pure database operations for folders"""
from supabase import Client
from domains.entities import Folder, FolderTitle

class FolderBaseRepository:
    """Base repository for folder database operations"""

    @staticmethod
    def get_folders_titles(
        client: Client,
        organization_id: str | None = None,
        parent_folder_ids: list[str] | None = None,
        user_id: str | None = None,
        or_conditions: list[str] | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[FolderTitle]:
        """
        Get folder titles with filtering.
        Pure database operation - no permission checks.
        """
        query = client.table("prompt_folders").select("id, title")

        # Apply OR conditions if provided (for workspace filters)
        if or_conditions:
            query = query.or_(",".join(or_conditions))
        elif organization_id:
            query = query.eq("organization_id", organization_id)
        elif user_id:
            query = query.eq("user_id", user_id).is_("organization_id", "null")

        # Parent folder filtering
        if parent_folder_ids is not None:
            if len(parent_folder_ids) == 0:
                query = query.is_("parent_folder_id", "null")
            else:
                query = query.in_("parent_folder_id", parent_folder_ids)

        query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
        response = query.execute()
        folders_data = response.data or []

        folders = [FolderTitle(**item) for item in folders_data]
        return folders

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def update_folder(
        client: Client,
        folder_id: str,
        title: dict[str, str] | None = None,
        description: dict[str, str] | None = None,
        parent_folder_id: str | None = None
    ) -> Folder | None:
        """Update folder fields"""
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if parent_folder_id is not None:
            update_data["parent_folder_id"] = parent_folder_id

        response = client.table("prompt_folders")\
            .update(update_data)\
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

    @staticmethod
    def delete_folder(client: Client, folder_id: str) -> bool:
        """Delete a folder"""
        response = client.table("prompt_folders").delete().eq("id", folder_id).execute()
        return len(response.data or []) > 0

    @staticmethod
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

    @staticmethod
    def update_pinned_folders(client: Client, user_id: str, folder_ids: list[str]) -> list[str]:
        """Update pinned folders for a user"""
        client.table("users_metadata")\
            .update({"pinned_folder_ids": folder_ids})\
            .eq("user_id", user_id)\
            .execute()

        return folder_ids
