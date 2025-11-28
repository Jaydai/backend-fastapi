"""Template version repository - handles version database operations"""

from supabase import Client

from domains.entities import TemplateVersion, TemplateVersionUpdate, VersionContent, VersionSummary


class TemplateVersionRepository:
    """Repository for template version database operations"""

    @staticmethod
    def get_versions(client: Client, template_id: str) -> list[TemplateVersion]:
        response = (
            client.table("prompt_templates_versions")
            .select("*")
            .eq("template_id", template_id)
            .order("created_at", desc=True)
            .execute()
        )

        versions = []
        for data in response.data or []:
            versions.append(TemplateVersion(data))

        return versions

    @staticmethod
    def get_versions_summary(client: Client, template_id: str, published: bool | None = None) -> list[VersionSummary]:
        query = (
            client.table("prompt_templates_versions")
            .select("id, name, slug, is_default, status, published, optimized_for")
            .eq("template_id", template_id)
        )
        if published is not None:
            query = query.eq("published", published)
        response = query.order("created_at", desc=True).execute()

        if not response.data:
            return []

        return [VersionSummary(**item) for item in response.data]

    @staticmethod
    def get_version_by_id(client: Client, version_id: int) -> VersionContent | None:
        response = client.table("prompt_templates_versions").select("id, content").eq("id", version_id).execute()

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
        description: dict[str, str] | None = None,
        status: str = "draft",
        optimized_for: list[str] | None = None,
    ) -> TemplateVersion:
        if not name:
            existing_versions = TemplateVersionRepository.get_versions(client, template_id)
            name = f"{len(existing_versions) + 1}.0"

        version_data = {
            "template_id": template_id,
            "author_id": author_id,
            "content": content,
            "name": name,
            "description": description,
            "status": status,
            "optimized_for": optimized_for,
        }

        response = client.table("prompt_templates_versions").insert(version_data).execute()

        data = response.data[0]
        return TemplateVersion(data)

    @staticmethod
    def set_default_version(client: Client, version_id: int, template_id: str) -> int | None:
        unset_default_response = (
            client.table("prompt_templates_versions")
            .update({"is_default": False})
            .eq("template_id", template_id)
            .execute()
        )
        if not unset_default_response.data:
            return None

        set_default_response = (
            client.table("prompt_templates_versions")
            .update({"is_default": True})
            .eq("id", version_id)
            .execute()
        )
        if not set_default_response.data:
            return None

        return version_id

    @staticmethod
    def update_version(
        client: Client,
        version_id: int,
        template_id: str,
        update_data: TemplateVersionUpdate
    ) -> TemplateVersionUpdate | None:
        """Update version fields. Handles is_default by unsetting other versions first."""

        if not update_data:
            return None
        
        data_to_update = {k: v for k, v in update_data.items() if v is not None}
        

        update_response = (
            client.table("prompt_templates_versions")
            .update(data_to_update)
            .eq("id", version_id)
            .eq("template_id", template_id)
            .execute()
        )

        print(f"❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️ update_response: {update_response}")

        if not update_response.data:
            return None

        return update_data
