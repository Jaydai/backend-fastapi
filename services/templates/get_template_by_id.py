from supabase import Client
from dtos import TemplateResponseDTO
from repositories.template_repository import TemplateRepository
from mappers.template_mapper import TemplateMapper


def get_template_by_id(
    client: Client,
    template_id: str,
    locale: str = "en"
) -> TemplateResponseDTO | None:
    template = TemplateRepository.get_template_by_id(client, template_id)
    if not template:
        return None

    versions = TemplateRepository.get_versions(client, template_id)
    comments = TemplateRepository.get_comments(client, template_id, locale)

    return TemplateMapper.entity_to_response_dto(template, versions, comments, locale)
