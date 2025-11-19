from supabase import Client
from dtos import (
    CreateTemplateDTO,
    UpdateTemplateDTO,
    CreateVersionDTO,
    TemplateVersionResponseDTO,
    TemplateListItemDTO,
    TemplateResponseDTO,
    UsageResponseDTO,
    TemplateTitleResponseDTO,
)
from repositories.template_repository import TemplateRepository
from mappers.template_mapper import TemplateMapper
from utils import localize_object
from domains.entities import TemplateVersion

class TemplateService:
    @staticmethod
    def get_all_templates_title() -> list[TemplateTitleResponseDTO]:
        templates = TemplateRepository.get_all_templates_title()
        return [
            TemplateTitleResponseDTO(**localize_object(template, "fr", ["title"]))
            for template in templates
        ]

    @staticmethod
    def get_templates(
        client: Client,
        user_id: str,
        locale: str = "en",
        workspace_type: str | None = None,
        organization_id: str | None = None,
        company_id: str | None = None,
        folder_id: int | None = None,
        tags: list[str] | None = None,
        published: bool | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[TemplateListItemDTO]:
        templates = TemplateRepository.get_templates(
            client,
            user_id,
            workspace_type,
            organization_id,
            company_id,
            folder_id,
            tags,
            published,
            limit,
            offset
        )

        return [TemplateMapper.entity_to_list_item_dto(t, locale) for t in templates]

    @staticmethod
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

    @staticmethod
    def create_template(
        client: Client,
        user_id: str,
        data: CreateTemplateDTO,
        locale: str = "en"
    ) -> TemplateResponseDTO:
        # TODO: remove workspace_type ?
        workspace_type = "user"
        if data.organization_id:
            workspace_type = "organization"
        elif data.company_id:
            workspace_type = "company"

        title_dict = TemplateMapper.ensure_localized_dict(data.title, locale)
        description_dict = TemplateMapper.ensure_localized_dict(data.description, locale) if data.description else None
        content_dict = TemplateMapper.ensure_localized_dict(data.content, locale)

        template = TemplateRepository.create_template(
            client,
            user_id,
            title_dict,
            description_dict,
            data.folder_id,
            data.organization_id,
            data.company_id,
            data.tags,
            workspace_type
        )

        try:
            version = TemplateRepository.create_version(
                client,
                template.id,
                user_id,
                content_dict,
                version_number="1.0",
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
        client: Client,
        template_id: str,
        data: UpdateTemplateDTO,
        locale: str = "en"
    ) -> TemplateResponseDTO | None:
        template = TemplateRepository.get_template_by_id(client, template_id)
        if not template:
            return None

        title_dict = TemplateMapper.ensure_localized_dict(data.title, locale) if data.title else None
        description_dict = TemplateMapper.ensure_localized_dict(data.description, locale) if data.description else None

        content_updated = data.content is not None
        status_updated = data.status is not None

        if content_updated or status_updated:
            if data.version_id:
                version_update_data = {}
                if content_updated:
                    version_update_data["content"] = TemplateMapper.ensure_localized_dict(data.content, locale)
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
                    content_dict = TemplateMapper.ensure_localized_dict(data.content, locale)
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
            version_number=data.version_number,
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
    ) -> list[TemplateListItemDTO]:
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