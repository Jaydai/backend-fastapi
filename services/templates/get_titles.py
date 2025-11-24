"""Get template titles service"""
from supabase import Client
from dtos import TemplateTitleResponseDTO
from repositories.templates import get_templates_titles as repo_get_templates_titles
from utils import localize_object


def get_templates_titles(
    client: Client,
    locale: str = "en",
    user_id: str | None = None,
    organization_id: str | None = None,
    folder_id: str | None = None,
    limit: int = 100,
    offset: int = 0
) -> list[TemplateTitleResponseDTO]:
    """
    Get template titles with localization.

    Args:
        client: Supabase client
        locale: Locale for localization
        user_id: Filter by user ID
        organization_id: Filter by organization ID
        folder_id: Filter by folder ID (overrides user/org)
        limit: Max results
        offset: Pagination offset

    Returns:
        List of localized template title DTOs
    """
    templates = repo_get_templates_titles(
        client,
        user_id=user_id,
        organization_id=organization_id,
        folder_id=folder_id,
        limit=limit,
        offset=offset
    )

    return [
        TemplateTitleResponseDTO(**localize_object(template.__dict__, locale, ["title"]))
        for template in templates
    ]
