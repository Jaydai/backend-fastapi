"""
Template Repository - Database Operations Layer
Handles all template-related database queries
"""
from supabase import Client
from datetime import datetime
from domains.entities import Template, TemplateTitle, TemplateVersion, TemplateComment


class TemplateRepository:
    """Repository for template database operations"""

    # ==================== TEMPLATE QUERIES ====================

    @staticmethod
    def get_templates_titles(
        client: Client,
        user_id: str | None = None,
        organization_id: str | None = None,
        folder_id: str | None = None,
        published_only: bool | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[TemplateTitle]:
        """
        Get template titles with filtering.
        Applies filters as provided by the service layer.
        """
        query = client.table("prompt_templates").select("id, title, folder_id")

        if user_id:
            query = query.eq("user_id", user_id)
        if organization_id:
            query = query.eq("organization_id", organization_id)
        if published_only is not None:
            query = query.eq("published", published_only)

        # Filter by folder_id:
        # - "ROOT" = only root templates (folder_id IS NULL)
        # - UUID string = templates in that folder
        # - None/not provided = ALL templates (for tree building)
        if folder_id == "ROOT":
            query = query.is_("folder_id", "null")
        elif folder_id is not None:
            query = query.eq("folder_id", folder_id)

        query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
        response = query.execute()
        templates_data = response.data or []

        return [TemplateTitle(**item) for item in templates_data]

    @staticmethod
    def get_template_by_id(client: Client, template_id: str) -> Template | None:
        """Get a single template by ID with all fields"""
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
            created_at=data["created_at"],
            updated_at=data.get("updated_at"),
            usage_count=data.get("usage_count", 0),
            last_used_at=data.get("last_used_at"),
            current_version_id=data.get("current_version_id"),
            is_published=data.get("is_published", False)
        )

    @staticmethod
    def get_template_metadata(client: Client, template_id: str) -> Template | None:
        """
        Get template metadata without content.
        Optimized for initial page load - fetches only metadata fields.
        """
        response = client.table("prompt_templates").select(
            "id, title, description, folder_id, organization_id, user_id, "
            "workspace_type, created_at, updated_at, tags, usage_count, "
            "current_version_id, is_free, is_published"
        ).eq("id", template_id).single().execute()

        if not response.data:
            return None

        # Add empty content field to satisfy Template entity
        data = response.data
        data["content"] = ""

        return Template(**data)

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
        if len(response.data or []) == 0:
            return None
        data = response.data[0]
        return Template(data)

    @staticmethod
    def update_template(
        client: Client,
        template_id: str,
        title: dict[str, str] | None = None,
        description: dict[str, str] | None = None,
        folder_id: str | None = None,
        tags: list[str] | None = None,
        current_version_id: int | None = None
    ) -> Template:
        """Update template metadata"""
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

        if len(response.data or []) == 0:
            return None
        data = response.data[0]
        return Template(data)

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
        """Increment usage count and update last_used_at"""
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

    @staticmethod
    def search_templates(
        client: Client,
        user_id: str,
        query: str,
        tags: list[str] | None = None,
        include_public: bool = True,
        limit: int = 50,
        offset: int = 0
    ) -> list[Template]:
        """Search templates by query and tags"""
        # TODO: Implement full-text search
        # For now, basic filter
        query_builder = client.table("prompt_templates").select("*")

        if not include_public:
            query_builder = query_builder.eq("user_id", user_id)

        if tags:
            query_builder = query_builder.contains("tags", tags)

        query_builder = query_builder.order("created_at", desc=True).range(offset, offset + limit - 1)
        response = query_builder.execute()

        return [Template(data) for data in (response.data or [])]

    @staticmethod
    def get_user_templates_count(client: Client, user_id: str) -> int:
        """Get count of templates owned by user"""
        query = client.table("prompt_templates").select("id").eq("user_id", user_id)
        response = query.execute()
        return len(response.data or [])

    @staticmethod
    def get_organization_templates_count(client: Client, organization_id: str) -> int:
        """Get count of templates in organization"""
        query = client.table("prompt_templates").select("id").eq("organization_id", organization_id)
        response = query.execute()
        return len(response.data or [])

    # ==================== VERSION OPERATIONS (LEGACY) ====================
    # These methods delegate to TemplateVersionRepository

    @staticmethod
    def get_versions(client: Client, template_id: str) -> list[TemplateVersion]:
        """Get all versions for a template (delegates to TemplateVersionRepository)"""
        from repositories.template_versions_repository import TemplateVersionRepository
        return TemplateVersionRepository.get_versions(client, template_id)

    @staticmethod
    def get_version_by_id(client: Client, version_id: int) -> TemplateVersion | None:
        """Get version by ID (delegates to TemplateVersionRepository)"""
        from repositories.template_versions_repository import TemplateVersionRepository
        return TemplateVersionRepository.get_version_by_id(client, version_id)

    @staticmethod
    def create_version(
        client: Client,
        template_id: str,
        author_id: str,
        content: dict[str, str],
        name: str | None = None,
        change_notes: dict[str, str] | None = None,
        status: str = "draft",
        optimized_for: list[str] | None = None
    ) -> TemplateVersion:
        """Create version (delegates to TemplateVersionRepository)"""
        from repositories.template_versions_repository import TemplateVersionRepository
        return TemplateVersionRepository.create_version(
            client, template_id, author_id, content, name, change_notes, status, optimized_for
        )

    @staticmethod
    def update_version(
        client: Client,
        version_id: int,
        template_id: str,
        content: dict[str, str] | None = None,
        status: str | None = None
    ) -> TemplateVersion | None:
        """Update version (delegates to TemplateVersionRepository)"""
        from repositories.template_versions_repository import TemplateVersionRepository
        return TemplateVersionRepository.update_version(client, version_id, template_id, content, status)

    @staticmethod
    def get_comments(client: Client, template_id: str, locale: str = "en") -> list[TemplateComment]:
        """Get comments for a template"""
        # TODO: Implement comments repository
        return []
