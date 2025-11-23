"""Template version repository - handles version database operations"""
from supabase import Client
from domains.entities import TemplateVersion, VersionSummary
from repositories.templates.versions import (
    get_versions,
    get_versions_summary,
    get_version_by_id,
    create_version,
    update_version,
    get_version_by_slug,
)

class TemplateVersionRepository:
    """Repository for template version database operations"""

    @staticmethod
    def get_versions(client: Client, template_id: str) -> list[TemplateVersion]:
        return get_versions(client, template_id)

    @staticmethod
    def get_versions_summary(client: Client, template_id: str) -> list[VersionSummary]:
        return get_versions_summary(client, template_id)

    @staticmethod
    def get_version_by_id(client: Client, version_id: int) -> TemplateVersion | None:
        return get_version_by_id(client, version_id)
    
    @staticmethod
    def get_version_by_slug(client:Client, template_id: str, slug: str) -> TemplateVersion | None:
        return get_version_by_slug(client, template_id, slug)

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
        return create_version(client, template_id, author_id, content, name, change_notes, status, optimized_for)

    @staticmethod
    def update_version(
        client: Client,
        version_id: int,
        template_id: str,
        content: dict[str, str] | None = None,
        status: str | None = None
    ) -> TemplateVersion | None:
        return update_version(client, version_id, template_id, content, status)

