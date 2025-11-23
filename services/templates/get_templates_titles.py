"""Template title service - handles business logic for template list operations"""
from supabase import Client
from dtos import TemplateTitleResponseDTO
from repositories import TemplateRepository
from utils import localize_object


def get_templates_titles(
    client: Client,
    locale: str = "en",
    organization_id: str | None = None,
    folder_ids: list[str] | None = None,
    published: bool | None = None,
    limit: int = 100,
    offset: int = 0
) -> list[TemplateTitleResponseDTO]:
    templates = TemplateRepository.get_templates_titles(
        client,
        organization_id=organization_id,
        folder_ids=folder_ids,
        published=published,
        limit=limit,
        offset=offset
    )
    return [
        TemplateTitleResponseDTO(**localize_object(template.__dict__, locale, ["title"]))
        for template in templates
    ]
