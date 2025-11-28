from supabase import Client

from domains.entities import TemplateVersion, VersionSummary
from dtos import CreateTemplateVersionDTO, CreateVersionDTO, TemplateVersionContentDTO, UpdateTemplateVersionDTO
from mappers.template_mapper import TemplateMapper
from repositories import TemplateVersionRepository
from services.locale_service import LocaleService


class TemplateVersionService:
    @staticmethod
    def get_version_by_id(
        client: Client, version_id: int, locale: str = LocaleService.DEFAULT_LOCALE
    ) -> TemplateVersionContentDTO | None:
        """Get a specific template version by its ID"""
        version = TemplateVersionRepository.get_version_by_id(client, version_id)
        if not version:
            return None
        return TemplateMapper.version_entity_to_content_dto(version, locale)

    def get_versions_summary(client: Client, template_id: str, published: bool | None = None) -> list[VersionSummary]:
        return TemplateVersionRepository.get_versions_summary(client, template_id, published)

    @staticmethod
    def create_version(
        client: Client,
        template_id: str,
        user_id: str,
        data: CreateVersionDTO,
        locale: str = LocaleService.DEFAULT_LOCALE,
    ) -> CreateTemplateVersionDTO:
        if data.copy_from_version_id:
            source_version = TemplateVersionRepository.get_version_by_id(client, data.copy_from_version_id)
            if not source_version:
                return None
            content_dict = source_version.content
        else:
            content_dict = LocaleService.ensure_localized_dict(data.content, locale) if data.content else {locale: ""}

        description_dict = (
            LocaleService.ensure_localized_dict(data.description, locale) if data.description else None
        )

        version = TemplateVersionRepository.create_version(
            client,
            template_id,
            user_id,
            content_dict,
            name=data.name,
            description=description_dict,
            status=data.status or "draft",
            optimized_for=data.optimized_for,
        )

        return TemplateMapper.version_entity_to_dto(version, locale)

    @staticmethod
    def update_version(
        client: Client,
        version_id: int,
        template_id: str,
        update_data: UpdateTemplateVersionDTO,
        locale: str = LocaleService.DEFAULT_LOCALE,
    ) -> UpdateTemplateVersionDTO | None:
        """Update version fields (content, description, status, is_default, published, optimized_for)"""
        # Convert content and description to localized dicts if provided
        if update_data.is_default is True:
            version_id = TemplateVersionRepository.set_default_version(client, version_id, template_id)
            if not version_id:
                return None
        content_dict = LocaleService.ensure_localized_dict(update_data.content, locale) if update_data.content is not None else None
        description_dict = (
            LocaleService.ensure_localized_dict(update_data.description, locale) if update_data.description is not None else None
        )

        update_data = {
            "content": content_dict,
            "description": description_dict,
            "status": update_data.status,
            "is_default": update_data.is_default,
            "published": update_data.published,
            "optimized_for": update_data.optimized_for,
        }

        updated_version = TemplateVersionRepository.update_version(
            client,
            version_id,
            template_id,
            update_data
        )

        if not updated_version:
            return None
        return TemplateMapper.update_version_entity_to_dto(updated_version, locale)

