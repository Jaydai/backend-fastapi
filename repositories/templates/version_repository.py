"""Template version repository - handles version database operations"""
from supabase import Client
from domains.entities import TemplateVersion

class TemplateVersionRepository:
    """Repository for template version database operations"""

    @staticmethod
    def get_versions(client: Client, template_id: str) -> list[TemplateVersion]:
        """Get all versions for a template"""
        response = client.table("prompt_templates_versions")\
            .select("*")\
            .eq("template_id", template_id)\
            .order("created_at", desc=True)\
            .execute()

        versions = []
        for data in response.data or []:
            versions.append(TemplateVersion(
                id=data["id"],
                template_id=data["template_id"],
                version_number=data.get("version_number", "1.0"),
                content=data.get("content", {}),
                description=data.get("description"),
                change_notes=data.get("change_notes"),
                author_id=data["author_id"],
                created_at=data["created_at"],
                updated_at=data.get("updated_at"),
                status=data.get("status", "draft"),
                is_current=data.get("is_current", False),
                is_published=data.get("is_published", False),
                usage_count=data.get("usage_count", 0),
                parent_version_id=data.get("parent_version_id"),
                optimized_for=data.get("optimized_for")
            ))

        return versions

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
            version_number=data.get("version_number", "1.0"),
            content=data.get("content", {}),
            description=data.get("description"),
            change_notes=data.get("change_notes"),
            author_id=data["author_id"],
            created_at=data["created_at"],
            updated_at=data.get("updated_at"),
            status=data.get("status", "draft"),
            is_current=data.get("is_current", False),
            is_published=data.get("is_published", False),
            usage_count=data.get("usage_count", 0),
            parent_version_id=data.get("parent_version_id"),
            optimized_for=data.get("optimized_for")
        )

    @staticmethod
    def create_version(
        client: Client,
        template_id: str,
        author_id: str,
        content: dict[str, str],
        version_number: str | None = None,
        change_notes: dict[str, str] | None = None,
        status: str = "draft",
        optimized_for: list[str] | None = None
    ) -> TemplateVersion:
        """Create a new template version"""
        # Auto-generate version number if not provided
        if not version_number:
            existing_versions = TemplateVersionRepository.get_versions(client, template_id)
            version_number = f"{len(existing_versions) + 1}.0"

        version_data = {
            "template_id": template_id,
            "author_id": author_id,
            "content": content,
            "version_number": version_number,
            "change_notes": change_notes,
            "status": status,
            "optimized_for": optimized_for
        }

        response = client.table("prompt_templates_versions")\
            .insert(version_data)\
            .execute()

        data = response.data[0]
        return TemplateVersion(
            id=data["id"],
            template_id=data["template_id"],
            version_number=data.get("version_number", "1.0"),
            content=data.get("content", {}),
            description=data.get("description"),
            change_notes=data.get("change_notes"),
            author_id=data["author_id"],
            created_at=data["created_at"],
            updated_at=data.get("updated_at"),
            status=data.get("status", "draft"),
            is_current=data.get("is_current", False),
            is_published=data.get("is_published", False),
            usage_count=data.get("usage_count", 0),
            parent_version_id=data.get("parent_version_id"),
            optimized_for=data.get("optimized_for")
        )

    @staticmethod
    def update_version(
        client: Client,
        version_id: int,
        template_id: str,
        content: dict[str, str] | None = None,
        status: str | None = None
    ) -> TemplateVersion | None:
        """Update a version"""
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
        return TemplateVersion(
            id=data["id"],
            template_id=data["template_id"],
            version_number=data.get("version_number", "1.0"),
            content=data.get("content", {}),
            description=data.get("description"),
            change_notes=data.get("change_notes"),
            author_id=data["author_id"],
            created_at=data["created_at"],
            updated_at=data.get("updated_at"),
            status=data.get("status", "draft"),
            is_current=data.get("is_current", False),
            is_published=data.get("is_published", False),
            usage_count=data.get("usage_count", 0),
            parent_version_id=data.get("parent_version_id"),
            optimized_for=data.get("optimized_for")
        )
