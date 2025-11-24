"""
Template Versions Repository - Database Operations Layer
Handles all template version-related database queries
"""
from supabase import Client
from dataclasses import dataclass
from domains.entities import TemplateVersion


@dataclass
class VersionSummary:
    """Minimal version data for version selector (without content)"""
    id: int
    name: dict[str, str]  # Localized name
    slug: str
    is_current: bool


class TemplateVersionRepository:
    """Repository for template version database operations"""

    # ==================== VERSION QUERIES ====================

    @staticmethod
    def get_versions(client: Client, template_id: str) -> list[TemplateVersion]:
        """Get all versions for a template ordered by creation date"""
        response = client.table("prompt_templates_versions")\
            .select("*")\
            .eq("template_id", template_id)\
            .order("created_at", desc=True)\
            .execute()

        versions = []
        print(response.data)
        for data in response.data or []:
            versions.append(TemplateVersion(
                id=data["id"],
                template_id=data["template_id"],
                name=data.get("name"),
                slug=data.get("slug"),
                content=data.get("content"),
                change_notes=data.get("change_notes"),
                author_id=data.get("author_id"),
                created_at=data.get("created_at"),
                updated_at=data.get("updated_at"),
                status=data.get("status"),
                is_current=data.get("is_current", False),
                is_published=data.get("is_published", False),
                usage_count=data.get("usage_count", 0),
                parent_version_id=data.get("parent_version_id"),
                optimized_for=data.get("optimized_for")
            ))

        return versions

    @staticmethod
    def get_versions_summary(client: Client, template_id: str) -> list[VersionSummary]:
        """
        Get version summaries without content.
        Optimized for version selector in UI.
        """
        response = client.table("prompt_templates_versions").select(
            "id, name, slug, is_current"
        ).eq("template_id", template_id).order("created_at", desc=True).execute()

        if not response.data:
            return []

        return [VersionSummary(**item) for item in response.data]

    @staticmethod
    def get_version_by_id(client: Client, version_id: int) -> TemplateVersion | None:
        """Get a specific version by ID"""
        response = client.table("prompt_templates_versions")\
            .select("*")\
            .eq("id", version_id)\
            .execute()

        if not response.data:
            return None

        data = response.data[0]
        return TemplateVersion(
            id=data["id"],
            template_id=data["template_id"],
            name=data.get("name"),
            slug=data.get("slug"),
            content=data.get("content"),
            change_notes=data.get("change_notes"),
            author_id=data.get("author_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            status=data.get("status"),
            is_current=data.get("is_current", False),
            is_published=data.get("is_published", False),
            usage_count=data.get("usage_count", 0),
            parent_version_id=data.get("parent_version_id"),
            optimized_for=data.get("optimized_for")
        )

    @staticmethod
    def get_version_by_slug(
        client: Client,
        template_id: str,
        slug: str
    ) -> TemplateVersion | None:
        """Get version by slug for a specific template"""
        response = client.table("prompt_templates_versions").select(
            "id, template_id, name, slug, content, change_notes, author_id, "
            "created_at, updated_at, status, is_current, is_published, "
            "usage_count, parent_version_id, optimized_for"
        ).eq("template_id", template_id).eq("slug", slug).single().execute()

        if not response.data:
            return None

        return TemplateVersion(**response.data)

    # ==================== VERSION MUTATIONS ====================

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
        """Create a new template version"""
        # Auto-generate version number if not provided
        if not name:
            existing_versions = TemplateVersionRepository.get_versions(client, template_id)
            name = f"{len(existing_versions) + 1}.0"

        version_data = {
            "template_id": template_id,
            "author_id": author_id,
            "content": content,
            "name": name,
            "change_notes": change_notes,
            "status": status,
            "optimized_for": optimized_for
        }

        response = client.table("prompt_templates_versions")\
            .insert(version_data)\
            .execute()

        data = response.data[0]
        return TemplateVersion(data)

    @staticmethod
    def update_version(
        client: Client,
        version_id: int,
        template_id: str,
        content: dict[str, str] | None = None,
        status: str | None = None
    ) -> TemplateVersion | None:
        """Update a template version"""
        update_data = {}
        if content is not None:
            update_data["content"] = content
        if status is not None:
            update_data["status"] = status

        response = client.table("prompt_templates_versions")\
            .update(update_data)\
            .eq("id", version_id)\
            .eq("template_id", template_id)\
            .execute()

        if not response.data:
            return None

        data = response.data[0]
        return TemplateVersion(data)

    @staticmethod
    def set_default_version(client: Client, template_id: str, version_id: int) -> bool:
        """
        Set a specific version as the current/default version for a template.
        Unsets all other versions first.
        """
        # Unset all other versions as current
        client.table("prompt_templates_versions").update({
            "is_current": False
        }).eq("template_id", template_id).execute()

        # Set this version as current
        client.table("prompt_templates_versions").update({
            "is_current": True
        }).eq("id", version_id).eq("template_id", template_id).execute()

        # Update the template's current_version_id
        client.table("prompt_templates").update({
            "current_version_id": version_id
        }).eq("id", template_id).execute()

        return True

    @staticmethod
    def delete_version(client: Client, template_id: str, version_id: int) -> bool:
        """Delete a specific template version"""
        response = (
            client.table("prompt_templates_versions")
            .delete()
            .eq("id", version_id)
            .eq("template_id", template_id)
            .execute()
        )

        return bool(response.data)
