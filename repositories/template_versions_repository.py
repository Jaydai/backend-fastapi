"""Template version repository - handles version database operations"""
from supabase import Client
from domains.entities import TemplateVersion, VersionSummary, VersionContent


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
        "id, name, slug, is_current, status, published, optimized_for"
        ).eq("template_id", template_id)
        if published is not None:
            query = query.eq("published", published)
        response = query.order("created_at", desc=True).execute()


        if not response.data:
            return []

        return [VersionSummary(**item) for item in response.data]

    @staticmethod
    def get_version_by_id(client: Client, version_id: int) -> VersionContent | None:
        response = client.table("prompt_templates_versions")\
        .select("id, content")\
        .eq("id", version_id)\
        .execute()

        if not response.data:
            return None

        data = response.data[0]
        return VersionContent(**data)
    
    @staticmethod
    def create_version(
        client: Client,
        template_id: str,
        author_id: str,
        content: dict[str, str],
        name: str | None = None,
        change_notes: dict[str, str] | None = None,
        status: str = "draft",
        optimized_for: list[str] | None = None,
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
        status: str | None = None,
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

    @staticmethod
    def update_version_status(
        client: Client,
        version_id: int,
        template_id: str,
        published: bool | None = None,
        status: str | None = None,
        is_current: bool | None = None
    ) -> VersionContent | None:
        """Update version status fields (published, status, is_current)"""
        # If setting as current, first unset all other versions
        if is_current is True:
            client.table("prompt_templates_versions")\
                .update({"is_current": False})\
                .eq("template_id", template_id)\
                .execute()

        # Build update data
        update_data = {}
        if published is not None:
            update_data["published"] = published
        if status is not None:
            update_data["status"] = status
        if is_current is not None:
            update_data["is_current"] = is_current

        if not update_data:
            # Nothing to update, just return current version
            return TemplateVersionRepository.get_version_by_id(client, version_id)

        response = client.table("prompt_templates_versions")\
            .update(update_data)\
            .eq("id", version_id)\
            .execute()

        if not response.data:
            return None

        return VersionContent(id=response.data[0]["id"], content=response.data[0].get("content", ""))

