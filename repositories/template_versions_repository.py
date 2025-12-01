"""Template version repository - handles version database operations"""

from dataclasses import asdict

from supabase import Client

from domains.entities import TemplateVersion, TemplateVersionUpdate, VersionDetails, VersionSummary


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
            .select("id, name, is_default, status, published, optimized_for")
            .eq("template_id", template_id)
        )
        if published is not None:
            query = query.eq("published", published)
        response = query.order("created_at", desc=True).execute()

        if not response.data:
            return []

        return [VersionSummary(**item) for item in response.data]

    @staticmethod
    def get_version_by_id(client: Client, version_id: int) -> VersionDetails | None:
        response = client.table("prompt_templates_versions").select("id, optimized_for, published, status, description, content").eq("id", version_id).execute()
        if not response.data:
            return None
        data = response.data[0]
        return VersionDetails(
            id=data["id"],
            optimized_for=data["optimized_for"],
            published=data["published"],
            status=data["status"],
            description=data["description"],
            content=data["content"],
        )

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
    ) -> bool:
        """Update version fields."""
        # Convert dataclass to dict and filter out None values
        data_dict = {k: v for k, v in asdict(update_data).items() if v is not None}
        print(f"💕💕💕 data_dict: {data_dict}")

        if not data_dict:
            print(f"💕💕💕💕💕💕💕💕💕💕💕💕 data_dict is empty")
            return False

        update_response = (
            client.table("prompt_templates_versions")
            .update(data_dict)
            .eq("id", version_id)
            .eq("template_id", template_id)
            .execute()
        )

        print(f"😁😁😁😁😁😁😁😁😁😁😁😁 update_response: {update_response}")

        return bool(update_response.data)

    @staticmethod
    def get_version_details(client: Client, version_id: int, template_id: str) -> dict | None:
        """Get version details including is_default status."""
        response = (
            client.table("prompt_templates_versions")
            .select("id, name, is_default")
            .eq("id", version_id)
            .eq("template_id", template_id)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    @staticmethod
    def delete_version(client: Client, version_id: int, template_id: str) -> bool:
        """Delete a template version."""
        response = (
            client.table("prompt_templates_versions")
            .delete()
            .eq("id", version_id)
            .eq("template_id", template_id)
            .execute()
        )

        return bool(response.data)
