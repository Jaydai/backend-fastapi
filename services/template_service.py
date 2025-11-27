from supabase import Client
from dtos import (
    CreateTemplateDTO,
    UpdateTemplateDTO,
    CreateVersionDTO,
    TemplateVersionResponseDTO,
    TemplateTitleResponseDTO,
    TemplateResponseDTO,
    UsageResponseDTO,
    TemplateCountsResponseDTO
)
from repositories import TemplateRepository, TemplateVersionRepository, PermissionRepository

from mappers.template_mapper import TemplateMapper
from services.templates import get_templates_titles, create_template, update_template
from services.locale_service import LocaleService

class TemplateService:
    @staticmethod
    def get_templates_titles(
        client: Client,
        user_id: str,
        locale: str = LocaleService.DEFAULT_LOCALE,
        workspace_type: str | None = None,
        organization_id: str | None = None,
        folder_id: str | None = None,
        published: bool | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[TemplateTitleResponseDTO]:
        """Get template titles with simplified signature"""
        return get_templates_titles(
            client=client,
            locale=locale,
            user_id=user_id,
            workspace_type=workspace_type,
            organization_id=organization_id,
            folder_id=folder_id,
            published=published,
            limit=limit,
            offset=offset
        )

    @staticmethod
    def get_template_by_id(
        client: Client,
        template_id: str,
        locale: str = LocaleService.DEFAULT_LOCALE
    ) -> TemplateResponseDTO | None:
        template = TemplateRepository.get_template_by_id(client, template_id)
        if not template:
            return None

        versions_summary = TemplateVersionRepository.get_versions_summary(client, template_id)

        return TemplateMapper.entity_to_response_dto(template, versions_summary, locale)



    @staticmethod
    def create_template(
        client: Client,
        user_id: str,
        data: CreateTemplateDTO,
        locale: str = LocaleService.DEFAULT_LOCALE
    ) -> TemplateResponseDTO:
        return create_template(client, user_id, data, locale)


    @staticmethod
    def update_template(
        client: Client,
        template_id: str,
        data: UpdateTemplateDTO,
        locale: str = LocaleService.DEFAULT_LOCALE
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
        locale: str = LocaleService.DEFAULT_LOCALE
    ) -> list[TemplateVersionResponseDTO]:
        versions = TemplateRepository.get_versions(client, template_id)
        return [TemplateMapper.version_entity_to_dto(v, locale) for v in versions]

    @staticmethod
    def create_version(
        client: Client,
        template_id: str,
        user_id: str,
        data: CreateVersionDTO,
        locale: str = LocaleService.DEFAULT_LOCALE
    ) -> TemplateVersionResponseDTO:
        if data.copy_from_version_id:
            source_version = TemplateRepository.get_version_by_id(client, data.copy_from_version_id)
            if not source_version:
                return None
            content_dict = source_version.content
        else:
            content_dict = LocaleService.ensure_localized_dict(data.content, locale) if data.content else {locale: ""}

        change_notes_dict = LocaleService.ensure_localized_dict(data.change_notes, locale) if data.change_notes else None

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
    def get_version_by_slug(
        client: Client,
        template_id: str,
        slug: str,
        locale: str = LocaleService.DEFAULT_LOCALE
    ) -> TemplateVersionResponseDTO | None:
        version = TemplateVersionRepository.get_version_by_slug(client, template_id, slug)
        if not version:
            return None

        return TemplateMapper.version_entity_to_dto(version, locale)


    @staticmethod
    def search_templates(
        client: Client,
        user_id: str,
        query: str,
        locale: str = LocaleService.DEFAULT_LOCALE,
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

    @staticmethod
    def get_templates_counts(client: Client, user_id: str) -> TemplateCountsResponseDTO:
        user_counts = TemplateRepository.get_user_templates_count(client, user_id)
        user_all_roles = PermissionRepository.get_user_all_roles(client, user_id)
        organization_counts = {}
        for role in user_all_roles:
            if role.organization_id:
                organization_counts[role.organization_id] = TemplateRepository.get_organization_templates_count(client, role.organization_id)
        return TemplateCountsResponseDTO(user_counts=user_counts, organization_counts=organization_counts)