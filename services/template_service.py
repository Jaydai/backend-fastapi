from services.template_version_service import TemplateVersionService
from supabase import Client
from dtos import (
    CreateTemplateDTO,
    UpdateTemplateDTO,
    TemplateTitleResponseDTO,
    TemplateResponseDTO,
    TemplateTitleResponseDTO,
    TemplateVersionResponseDTO,
    UpdateTemplateDTO,
    UsageResponseDTO,
)
from repositories import TemplateRepository, PermissionRepository, TemplateVersionRepository
from mappers.template_mapper import TemplateMapper
from services.locale_service import LocaleService
from services.templates import create_template, get_templates_titles, update_template


class TemplateService:
    @staticmethod
    def get_templates_titles(
        client: Client,
        user_id: str,
        locale: str = LocaleService.DEFAULT_LOCALE,
        organization_id: str | None = None,
        folder_id: str | None = None,
        published: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[TemplateTitleResponseDTO]:
        """Get template titles with simplified signature"""
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

        templates = TemplateRepository.get_templates_titles(
            client,
            user_id=filter_user_id,
            organization_id=filter_org_id,
            published=published,
            limit=limit,
            offset=offset,
        )

        return [
            TemplateTitleResponseDTO(**LocaleService.localize_object(template.__dict__, locale, ["title"]))
            for template in templates
        ]

    @staticmethod
    def get_template_by_id(
        client: Client,
        template_id: str,
        published: bool | None = None,
        locale: str = LocaleService.DEFAULT_LOCALE,
    ) -> TemplateResponseDTO | None:
        template = TemplateRepository.get_template_by_id(client, template_id)
        if not template:
            return None

        versions_summary = TemplateVersionService.get_versions_summary(client, template_id, published)

        if published is not None and len(versions_summary) == 0:
            return None

        return TemplateMapper.entity_to_response_dto(template, versions_summary, locale)

    @staticmethod
    def create_template(
        client: Client, user_id: str, data: CreateTemplateDTO, locale: str = LocaleService.DEFAULT_LOCALE
    ) -> TemplateResponseDTO:
        workspace_type = "user"
        if data.organization_id:
            workspace_type = "organization"

        title_dict = LocaleService.ensure_localized_dict(data.title, locale)
        description_dict = LocaleService.ensure_localized_dict(data.description, locale) if data.description else None
        content_dict = LocaleService.ensure_localized_dict(data.content, locale)

        template = TemplateRepository.create_template(
            client,
            user_id,
            title_dict,
            description_dict,
            data.folder_id,
            data.organization_id,
            data.tags,
            workspace_type
        )

        try:
            version = TemplateVersionRepository.create_version(
                client,
                template.id,
                user_id,
                content_dict,
                name="1.0",
                change_notes=None,
                status="draft" if workspace_type != "user" else "published",
                optimized_for=data.optimized_for
            )

            TemplateRepository.update_template(client, template.id, current_version_id=version.id)

        except Exception as e:
            TemplateRepository.delete_template(client, template.id)
            raise Exception(f"Failed to create template version: {str(e)}")

        return TemplateService.get_template_by_id(client, template.id, locale)

    @staticmethod
    def update_template(
        client: Client, template_id: str, data: UpdateTemplateDTO, locale: str = LocaleService.DEFAULT_LOCALE
    ) -> TemplateResponseDTO | None:
        template = TemplateRepository.get_template_by_id(client, template_id)
        if not template:
            return None

        title_dict = LocaleService.ensure_localized_dict(data.title, locale) if data.title else None
        description_dict = LocaleService.ensure_localized_dict(data.description, locale) if data.description else None

        content_updated = data.content is not None
        status_updated = data.status is not None

        if content_updated or status_updated:
            if data.version_id:
                version_update_data = {}
                if content_updated:
                    version_update_data["content"] = LocaleService.ensure_localized_dict(data.content, locale)
                if status_updated:
                    version_update_data["status"] = data.status

                version = TemplateRepository.update_version(
                    client,
                    data.version_id,
                    template_id,
                    content=version_update_data.get("content"),
                    status=version_update_data.get("status")
                )

                if not version:
                    return None
            else:
                if content_updated:
                    content_dict = LocaleService.ensure_localized_dict(data.content, locale)
                    version = TemplateRepository.create_version(
                        client,
                        template_id,
                        template.user_id,
                        content_dict,
                        change_notes=None,
                        status=data.status or "draft"
                    )
                    TemplateRepository.update_template(
                        client,
                        template_id,
                        title=title_dict,
                        description=description_dict,
                        folder_id=data.folder_id,
                        tags=data.tags,
                        current_version_id=version.id
                    )

        if not content_updated and not status_updated:
            TemplateRepository.update_template(
                client,
                template_id,
                title=title_dict,
                description=description_dict,
                folder_id=data.folder_id,
                tags=data.tags,
                current_version_id=data.current_version_id
            )

        if data.is_pinned is not None:
            TemplateRepository.update_pinned_status(client, template.user_id, template_id, data.is_pinned)

        return TemplateService.get_template_by_id(client, template_id, locale)

    @staticmethod
    def delete_template(client: Client, template_id: str) -> bool:
        return TemplateRepository.delete_template(client, template_id)

    @staticmethod
    def increment_usage(client: Client, template_id: str) -> UsageResponseDTO:
        new_count = TemplateRepository.increment_usage(client, template_id)
        return UsageResponseDTO(usage_count=new_count)


    @staticmethod
    def search_templates(
        client: Client,
        user_id: str,
        query: str,
        locale: str = LocaleService.DEFAULT_LOCALE,
        tags: list[str] | None = None,
        include_public: bool = True,
        limit: int = 50,
        offset: int = 0,
    ) -> list[TemplateTitleResponseDTO]:
        templates = TemplateRepository.search_templates(client, user_id, query, tags, include_public, limit, offset)
        return [TemplateMapper.entity_to_list_item_dto(t, locale) for t in templates]

    @staticmethod
    def get_templates_counts(client: Client, user_id: str) -> TemplateCountsResponseDTO:
        user_counts = TemplateRepository.get_user_templates_count(client, user_id)
        user_all_roles = PermissionRepository.get_user_all_roles(client, user_id)
        organization_counts = {}
        for role in user_all_roles:
            if role.organization_id:
                organization_counts[role.organization_id] = TemplateRepository.get_organization_templates_count(
                    client, role.organization_id
                )
        return TemplateCountsResponseDTO(user_counts=user_counts, organization_counts=organization_counts)
