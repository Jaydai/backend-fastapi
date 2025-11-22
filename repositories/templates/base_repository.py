"""Template repository - handles pure database operations for templates"""
from supabase import Client
from domains.entities import Template, TemplateTitle

class TemplateBaseRepository:
    """Base repository for template database operations"""

    @staticmethod
    def get_templates_titles(
        client: Client,
        organization_id: str | None = None,
        folder_ids: list[str] | None = None,
        published: bool | None = None,
        user_id: str | None = None,
        or_conditions: list[str] | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[TemplateTitle]:
        """
        Get template titles with filtering.
        Pure database operation - no permission checks.

        Args:
            client: Supabase client
            organization_id: Filter by organization
            folder_ids: Filter by folder IDs (empty list = root only, None = all)
            published: Filter by published status
            user_id: Filter by user_id
            or_conditions: OR conditions for complex filters (e.g., ["user_id.eq.xxx", "organization_id.eq.yyy"])
            limit: Max results
            offset: Pagination offset
        """
        query = client.table("prompt_templates").select("id, title")

        # Apply OR conditions if provided (for workspace filters)
        if or_conditions:
            query = query.or_(",".join(or_conditions))
        elif organization_id:
            query = query.eq("organization_id", organization_id)
        elif user_id:
            query = query.eq("user_id", user_id).is_("organization_id", "null")

        # Folder filtering
        if folder_ids is not None:
            if len(folder_ids) == 0:
                query = query.is_("folder_id", "null")
            else:
                query = query.in_("folder_id", folder_ids)

        # Published filter
        if published is not None:
            # Need to check if template has published version
            # This requires a subquery or join - for now, we'll handle this differently
            pass

        query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
        response = query.execute()
        templates_data = response.data or []

        templates = [TemplateTitle(**item) for item in templates_data]
        return templates

    @staticmethod
    def get_template_by_id(client: Client, template_id: str) -> Template | None:
        """Get a single template by ID"""
        response = client.table("prompt_templates")\
            .select("*")\
            .eq("id", template_id)\
            .execute()

        if not response.data:
            return None

        data = response.data[0]
        return Template(
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
        )

    @staticmethod
    def create_template(
        client: Client,
        user_id: str,
        title: dict[str, str],
        description: dict[str, str] | None,
        folder_id: str | None,
        organization_id: str | None,
        tags: list[str] | None,
        workspace_type: str
    ) -> Template:
        """Create a new template"""
        template_data = {
            "user_id": user_id,
            "title": title,
            "description": description,
            "folder_id": folder_id,
            "organization_id": organization_id,
            "tags": tags or [],
            "workspace_type": workspace_type
        }

        response = client.table("prompt_templates").insert(template_data).execute()
        data = response.data[0]

        return Template(
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
        )

    @staticmethod
    def update_template(
        client: Client,
        template_id: str,
        title: dict[str, str] | None = None,
        description: dict[str, str] | None = None,
        folder_id: str | None = None,
        tags: list[str] | None = None,
        current_version_id: int | None = None
    ) -> bool:
        """Update template fields"""
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if folder_id is not None:
            update_data["folder_id"] = folder_id
        if tags is not None:
            update_data["tags"] = tags
        if current_version_id is not None:
            update_data["current_version_id"] = current_version_id

        response = client.table("prompt_templates")\
            .update(update_data)\
            .eq("id", template_id)\
            .execute()

        return len(response.data or []) > 0

    @staticmethod
    def delete_template(client: Client, template_id: str) -> bool:
        """Delete a template"""
        response = client.table("prompt_templates")\
            .delete()\
            .eq("id", template_id)\
            .execute()

        return len(response.data or []) > 0

    @staticmethod
    def increment_usage(client: Client, template_id: str) -> int:
        """Increment template usage count and return new count"""
        from datetime import datetime

        response = client.table("prompt_templates")\
            .select("usage_count")\
            .eq("id", template_id)\
            .execute()

        if not response.data:
            return 0

        current_count = response.data[0].get("usage_count", 0)
        new_count = current_count + 1

        client.table("prompt_templates")\
            .update({
                "usage_count": new_count,
                "last_used_at": datetime.utcnow().isoformat()
            })\
            .eq("id", template_id)\
            .execute()

        return new_count

    @staticmethod
    def update_pinned_status(
        client: Client,
        user_id: str,
        template_id: str,
        is_pinned: bool
    ) -> bool:
        """Update pinned status in user metadata"""
        response = client.table("users_metadata")\
            .select("pinned_template_ids")\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        if not response.data:
            return False

        current_pinned = response.data.get("pinned_template_ids") or []

        if is_pinned and template_id not in current_pinned:
            current_pinned.append(template_id)
        elif not is_pinned and template_id in current_pinned:
            current_pinned.remove(template_id)

        client.table("users_metadata")\
            .update({"pinned_template_ids": current_pinned})\
            .eq("user_id", user_id)\
            .execute()

        return True
