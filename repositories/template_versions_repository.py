"""Template version repository - handles version database operations"""
from supabase import Client
from domains.entities import TemplateVersion, VersionSummary


class TemplateVersionRepository:
    """Repository for template version database operations"""

    @staticmethod
    def get_versions(client: Client, template_id: str) -> list[TemplateVersion]:
        response = client.table("prompt_templates_versions")\
            .select("*")\
            .eq("template_id", template_id)\
            .order("created_at", desc=True)\
            .execute()

        versions = []
        for data in response.data or []:
            versions.append(TemplateVersion(data))

        return versions

    @staticmethod
    def get_versions_summary(client: Client, template_id: str, published: bool | None = None) -> list[VersionSummary]:
        query = client.table("prompt_templates_versions").select(
        "id, name, slug, is_current, status"
        ).eq("template_id", template_id)
        if published is not None:
            query = query.eq("published", published)
        response = query.order("created_at", desc=True).execute()


        if not response.data:
            return []

        return [VersionSummary(**item) for item in response.data]

    @staticmethod
    def get_version_by_id(client: Client, version_id: int) -> TemplateVersion | None:
        response = client.table("prompt_templates_versions")\
        .select("*")\
        .eq("id", version_id)\
        .execute()

        if not response.data:
            return None

        data = response.data[0]
        return TemplateVersion(data)
    
    @staticmethod
    def get_version_by_slug(client:Client, template_id: str, slug: str) -> TemplateVersion | None:
        response = client.table("prompt_templates_versions").select(
            "id, template_id, name, slug, content, change_notes, author_id, "
            "created_at, updated_at, status, is_current, published, "
            "usage_count, parent_version_id, optimized_for"
        ).eq("template_id", template_id).eq("slug", slug).single().execute()

        if not response.data:
            return None

        return TemplateVersion(**response.data)

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
        if not name:
            existing_versions = get_versions(client, template_id)
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

