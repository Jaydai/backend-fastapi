from supabase import Client

from domains.entities import VersionSummary
from dtos import CreateTemplateVersionDTO, CreateVersionDTO, TemplateVersionContentDTO
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

        change_notes_dict = (
            LocaleService.ensure_localized_dict(data.change_notes, locale) if data.change_notes else None
        )

        version = TemplateVersionRepository.create_version(
            client,
            template_id,
            user_id,
            content_dict,
            name=data.name,
            change_notes=change_notes_dict,
            status=data.status or "draft",
            optimized_for=data.optimized_for,
        )

        return TemplateMapper.version_entity_to_dto(version, locale)

    @staticmethod
    def update_version_status(
        client: Client,
        version_id: int,
        template_id: str,
        published: bool | None = None,
        status: str | None = None,
        is_current: bool | None = None,
        locale: str = LocaleService.DEFAULT_LOCALE,
    ) -> TemplateVersionContentDTO | None:
        """Update version status fields and optionally set as current"""
        version = TemplateVersionRepository.update_version_status(
            client, version_id, template_id, published=published, status=status, is_current=is_current
        )

        if not version:
            return None

        # If setting as current, also update the template's current_version_id
        if is_current is True:
            client.table("prompt_templates").update({"current_version_id": version_id}).eq("id", template_id).execute()

        return TemplateMapper.version_entity_to_content_dto(version, locale)
