"""Get template titles service"""
from supabase import Client
from dtos import TemplateTitleResponseDTO
from repositories.templates import get_templates_titles as repo_get_templates_titles
from services.locale_service import LocaleService


def get_templates_titles(
    client: Client,
    locale: str = LocaleService.DEFAULT_LOCALE,
    user_id: str | None = None,
    organization_id: str | None = None,
    folder_id: str | None = None,
    published: bool | None = None,
    limit: int = 100,
    offset: int = 0
) -> list[TemplateTitleResponseDTO]:
    # Business logic: Determine which filters to apply based on priority
    filter_user_id = None
    filter_org_id = None
    filter_folder_id = folder_id

    if folder_id is not None:
        # Priority 1: Filter by folder only
        pass
    elif organization_id:
        # Priority 2: Filter by organization only
        filter_org_id = organization_id
    elif user_id:
        # Priority 3: Filter by user only
        filter_user_id = user_id
    # Priority 4: No filters (RLS handles access)

    templates = repo_get_templates_titles(
        client,
        user_id=filter_user_id,
        organization_id=filter_org_id,
        folder_id=filter_folder_id,
        published=published,
        limit=limit,
        offset=offset
    )

    return [
        TemplateTitleResponseDTO(**LocaleService.localize_object(template.__dict__, locale, ["title"]))
        for template in templates
    ]
