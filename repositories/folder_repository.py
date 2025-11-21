from supabase import Client
from domains.entities import Folder

class FolderRepository:
    @staticmethod
    def _get_user_metadata(client: Client, user_id: str) -> dict:
        response = client.table("users_metadata")\
            .select("*")\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        if not response.data:
            return {"organization_ids": [], "roles": {}}

        return response.data

    @staticmethod
    def get_folders(
        client: Client,
        user_id: str,
        workspace_type: str | None = None,
        organization_id: str | None = None,
        parent_folder_id: str | None = None
    ) -> list[Folder]:
        query = client.table("prompt_folders").select("*")

        if workspace_type == "all" or (not workspace_type and not organization_id):
            user_metadata = FolderRepository._get_user_metadata(client, user_id)
            conditions = [f"user_id.eq.{user_id}"]

            roles = user_metadata.get("roles") or {}
            org_roles = roles.get("organizations", {}) if isinstance(roles, dict) else {}
            if org_roles:
                for org_id in org_roles.keys():
                    conditions.append(f"organization_id.eq.{org_id}")

            query = query.or_(",".join(conditions))
        elif workspace_type == "user":
            query = query.eq("user_id", user_id).is_("organization_id", "null")
        elif workspace_type == "organization":
            user_metadata = FolderRepository._get_user_metadata(client, user_id)
            roles = user_metadata.get("roles") or {}
            org_roles = roles.get("organizations", {}) if isinstance(roles, dict) else {}

            if organization_id:
                if organization_id not in org_roles:
                    return []
                query = query.eq("organization_id", organization_id)
            else:
                if not org_roles:
                    return []
                query = query.in_("organization_id", list(org_roles.keys()))

        if parent_folder_id is not None:
            if parent_folder_id == "root":
                query = query.is_("parent_folder_id", "null")
            else:
                query = query.eq("parent_folder_id", parent_folder_id)

        query = query.order("created_at", desc=True)

        response = query.execute()

        folders = []
        for data in response.data or []:
            folders.append(Folder(
                id=data["id"],
                title=data.get("title", {}),
                description=data.get("description"),
                user_id=data.get("user_id"),
                organization_id=data.get("organization_id"),
                parent_folder_id=data.get("parent_folder_id"),
                workspace_type=data["workspace_type"],
                created_at=data["created_at"],
                updated_at=data.get("updated_at")
            ))

        return folders

    @staticmethod
    def get_folder_by_id(client: Client, folder_id: str) -> Folder | None:
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
        response = client.table("prompt_folders").delete().eq("id", folder_id).execute()
        return len(response.data or []) > 0

    @staticmethod
    def get_pinned_folder_ids(client: Client, user_id: str) -> list[str]:
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
    def pin_folder(client: Client, user_id: str, folder_id: str) -> list[str]:
        current_pinned = FolderRepository.get_pinned_folder_ids(client, user_id)

        if folder_id not in current_pinned:
            current_pinned.append(folder_id)

        client.table("users_metadata")\
            .update({"pinned_folder_ids": current_pinned})\
            .eq("user_id", user_id)\
            .execute()

        return current_pinned

    @staticmethod
    def unpin_folder(client: Client, user_id: str, folder_id: str) -> list[str]:
        current_pinned = FolderRepository.get_pinned_folder_ids(client, user_id)

        if folder_id in current_pinned:
            current_pinned.remove(folder_id)

        client.table("users_metadata")\
            .update({"pinned_folder_ids": current_pinned})\
            .eq("user_id", user_id)\
            .execute()

        return current_pinned

    @staticmethod
    def update_pinned_folders(client: Client, user_id: str, folder_ids: list[str]) -> list[str]:
        client.table("users_metadata")\
            .update({"pinned_folder_ids": folder_ids})\
            .eq("user_id", user_id)\
            .execute()

        return folder_ids

    @staticmethod
    def get_root_items(
        client: Client,
        user_id: str,
        workspace_type: str | None = None,
        organization_id: str | None = None
    ) -> dict:
        from repositories.template_repository import TemplateRepository

        folders = FolderRepository.get_folders(
            client, user_id, workspace_type, organization_id, "root"
        )

        templates_query = client.table("prompt_templates")\
            .select("*")\
            .is_("folder_id", "null")

        if workspace_type == "all" or (not workspace_type and not organization_id):
            user_metadata = FolderRepository._get_user_metadata(client, user_id)
            conditions = [f"user_id.eq.{user_id}"]

            roles = user_metadata.get("roles") or {}
            org_roles = roles.get("organizations", {}) if isinstance(roles, dict) else {}
            if org_roles:
                for org_id in org_roles.keys():
                    conditions.append(f"organization_id.eq.{org_id}")

            templates_query = templates_query.or_(",".join(conditions))
        elif workspace_type == "user":
            templates_query = templates_query.eq("user_id", user_id)\
                .is_("organization_id", "null")
        elif workspace_type == "organization":
            user_metadata = FolderRepository._get_user_metadata(client, user_id)
            roles = user_metadata.get("roles") or {}
            org_roles = roles.get("organizations", {}) if isinstance(roles, dict) else {}

            if organization_id:
                if organization_id not in org_roles:
                    templates_query = templates_query.eq("id", "impossible-id")
                else:
                    templates_query = templates_query.eq("organization_id", organization_id)
            else:
                if org_roles:
                    templates_query = templates_query.in_("organization_id", list(org_roles.keys()))
                else:
                    templates_query = templates_query.eq("id", "impossible-id")

        templates_query = templates_query.order("created_at", desc=True)
        templates_response = templates_query.execute()

        templates = []
        for data in templates_response.data or []:
            from domains.entities import Template
            templates.append(Template(
                id=data["id"],
                title=data.get("title", {}),
                description=data.get("description"),
                folder_id=data.get("folder_id"),
                organization_id=data.get("organization_id"),
                user_id=data["user_id"],
                workspace_type=data["workspace_type"],
                created_at=data["created_at"],
                updated_at=data.get("updated_at"),
                tags=data.get("tags"),
                usage_count=data.get("usage_count", 0),
                last_used_at=data.get("last_used_at"),
                current_version_id=data.get("current_version_id"),
                is_free=data.get("is_free", True),
                is_published=data.get("is_published", False)
            ))

        return {"folders": folders, "templates": templates}

    @staticmethod
    def get_folder_items(client: Client, folder_id: str) -> dict:
        folders_response = client.table("prompt_folders")\
            .select("*")\
            .eq("parent_folder_id", folder_id)\
            .order("created_at", desc=True)\
            .execute()

        folders = []
        for data in folders_response.data or []:
            folders.append(Folder(
                id=data["id"],
                title=data.get("title", {}),
                description=data.get("description"),
                user_id=data.get("user_id"),
                organization_id=data.get("organization_id"),
                parent_folder_id=data.get("parent_folder_id"),
                workspace_type=data["workspace_type"],
                created_at=data["created_at"],
                updated_at=data.get("updated_at")
            ))

        templates_response = client.table("prompt_templates")\
            .select("*")\
            .eq("folder_id", folder_id)\
            .order("created_at", desc=True)\
            .execute()

        templates = []
        for data in templates_response.data or []:
            from domains.entities import Template
            templates.append(Template(
                id=data["id"],
                title=data.get("title", {}),
                description=data.get("description"),
                folder_id=data.get("folder_id"),
                organization_id=data.get("organization_id"),
                user_id=data["user_id"],
                workspace_type=data["workspace_type"],
                created_at=data["created_at"],
                updated_at=data.get("updated_at"),
                tags=data.get("tags"),
                usage_count=data.get("usage_count", 0),
                last_used_at=data.get("last_used_at"),
                current_version_id=data.get("current_version_id"),
                is_free=data.get("is_free", True),
                is_published=data.get("is_published", False)
            ))

        return {"folders": folders, "templates": templates}
