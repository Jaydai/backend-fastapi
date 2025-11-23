from supabase import Client
from dtos import (
    CreateTemplateDTO,
    UpdateTemplateDTO,
    CreateVersionDTO,
    TemplateVersionResponseDTO,
    TemplateTitleResponseDTO,
    TemplateResponseDTO,
    UsageResponseDTO,
    TemplateTitleResponseDTO,
    OrganizationTemplateTitleDTO,
)
from repositories.template_repository import TemplateRepository
from mappers.template_mapper import TemplateMapper
from utils import localize_object
from domains.entities import TemplateVersion
from services.templates import get_templates_titles, get_template_by_id, create_template, update_template

class TemplateService:

    @staticmethod
    def get_templates_titles(
        client: Client,
        locale: str = "en",
        user_id: str | None = None,
        organization_id: str | None = None,
        folder_ids: list[str] | None = None,
        published: bool | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[TemplateTitleResponseDTO]:
        return get_templates_titles(client, locale, organization_id, folder_ids, published, user_id, limit, offset)

    @staticmethod
    def get_template_by_id(
        client: Client,
        template_id: str,
        locale: str = "en"
    ) -> TemplateResponseDTO | None:
        return get_template_by_id(client, template_id, locale)


    @staticmethod
    def create_template(
        client: Client,
        user_id: str,
        data: CreateTemplateDTO,
        locale: str = "en"
    ) -> TemplateResponseDTO:
        return create_template(client, user_id, data, locale)


    @staticmethod
    def update_template(
        client: Client,
        template_id: str,
        data: UpdateTemplateDTO,
        locale: str = "en"
    ) -> TemplateResponseDTO | None:
        return update_template(client, template_id, data, locale)


    @staticmethod
    def delete_template(client: Client, template_id: str) -> bool:
        return TemplateRepository.delete_template(client, template_id)

    @staticmethod
    def increment_usage(client: Client, template_id: str) -> UsageResponseDTO:
        new_count = TemplateRepository.increment_usage(client, template_id)
        return UsageResponseDTO(usage_count=new_count)

    @staticmethod
    def get_versions(
        client: Client,
        template_id: str,
        locale: str = "en"
    ) -> list[TemplateVersionResponseDTO]:
        versions = TemplateRepository.get_versions(client, template_id)
        return [TemplateMapper.version_entity_to_dto(v, locale) for v in versions]

    @staticmethod
    def create_version(
        client: Client,
        template_id: str,
        user_id: str,
        data: CreateVersionDTO,
        locale: str = "en"
    ) -> TemplateVersionResponseDTO:
        if data.copy_from_version_id:
            source_version = TemplateRepository.get_version_by_id(client, data.copy_from_version_id)
            if not source_version:
                return None
            content_dict = source_version.content
        else:
            content_dict = TemplateMapper.ensure_localized_dict(data.content, locale) if data.content else {locale: ""}

        change_notes_dict = TemplateMapper.ensure_localized_dict(data.change_notes, locale) if data.change_notes else None

        version = TemplateRepository.create_version(
            client,
            template_id,
            user_id,
            content_dict,
            name=data.name,
            change_notes=change_notes_dict,
            status=data.status or "draft",
            optimized_for=data.optimized_for
        )

        return TemplateMapper.version_entity_to_dto(version, locale)

    @staticmethod
    def search_templates(
        client: Client,
        user_id: str,
        query: str,
        locale: str = "en",
        tags: list[str] | None = None,
        include_public: bool = True,
        limit: int = 50,
        offset: int = 0
    ) -> list[TemplateTitleResponseDTO]:
        templates = TemplateRepository.search_templates(
            client,
            user_id,
            query,
            tags,
            include_public,
            limit,
            offset
        )

        return [TemplateMapper.entity_to_list_item_dto(t, locale) for t in templates]
