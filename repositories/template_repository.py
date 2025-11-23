"""Template repository - handles pure database operations for templates"""
from supabase import Client
from domains.entities import Template, TemplateTitle, TemplateVersion, TemplateComment
from repositories.templates import get_templates_titles, get_template_by_id, create_template, update_template, delete_template, increment_usage, update_pinned_status
from repositories.template_versions_repository import TemplateVersionRepository

class TemplateRepository:
    """Base repository for template database operations"""

    @staticmethod
    def get_templates_titles(
        client: Client,
        organization_id: str | None = None,
        folder_ids: list[str] | None = None,
        published: bool | None = None,
        user_id: str | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[TemplateTitle]:
        return get_templates_titles(client, organization_id, folder_ids, published, user_id, limit, offset)


    @staticmethod
    def get_template_by_id(client: Client, template_id: str) -> Template | None:
       return get_template_by_id(client, template_id)

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
        return create_template(client, user_id, title, description, folder_id, organization_id, tags, workspace_type)
       


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
        return update_template(client, template_id, title, description, folder_id, tags, current_version_id)


    @staticmethod
    def delete_template(client: Client, template_id: str) -> bool:
        return delete_template(client, template_id)

    @staticmethod
    def increment_usage(client: Client, template_id: str) -> int:
        return increment_usage(client, template_id)

    @staticmethod
    def update_pinned_status(
        client: Client,
        user_id: str,
        template_id: str,
        is_pinned: bool
    ) -> bool:
        return update_pinned_status(client, user_id, template_id, is_pinned)

    @staticmethod
    def get_versions(client: Client, template_id: str) -> list[TemplateVersion]:
        return TemplateVersionRepository.get_versions(client, template_id)

    @staticmethod
    def get_comments(client: Client, template_id: str, locale: str = "en") -> list[TemplateComment]:
        # TODO: Implement comments repository
        return []