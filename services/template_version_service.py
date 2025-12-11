from supabase import Client

from domains.entities import TemplateVersionUpdate, VersionSummary
from dtos import CreateTemplateVersionDTO, CreateVersionDTO, TemplateVersionDTO, UpdateTemplateVersionDTO
from mappers.template_mapper import TemplateMapper
from repositories import TemplateVersionRepository
from services.locale_service import LocaleService


class TemplateVersionService:
    @staticmethod
    def get_version_by_id(
        client: Client, version_id: int, locale: str = LocaleService.DEFAULT_LOCALE
    ) -> TemplateVersionDTO | None:
        """Get a specific template version by its ID"""
        version = TemplateVersionRepository.get_version_by_id(client, version_id)
        if not version:
            return None
        return TemplateMapper.version_entity_to_content_dto(version, locale)

    @staticmethod
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
        print(f"💕💕💕 update_data: {update_data}")
        # Handle setting as default first
        if update_data.is_default is True:
            result = TemplateVersionRepository.set_default_version(client, version_id, template_id)
            if not result:
                return None

        # Convert content and description to localized dicts if provided
        content_dict = LocaleService.ensure_localized_dict(update_data.content, locale) if update_data.content is not None else None
        description_dict = (
            LocaleService.ensure_localized_dict(update_data.description, locale) if update_data.description is not None else None
        )

        # Create entity for repository
        version_update = TemplateVersionUpdate(
            name=update_data.name,
            content=content_dict,
            description=description_dict,
            status=update_data.status,
            is_default=None,  # Already handled above
            published=update_data.published,
            optimized_for=update_data.optimized_for,
        )

        # Only call update if there's something to update
        # We consider a field "provided" if it's not None (including if it's False or 0, which count as provided)
        has_updates = any(
            field is not None
            for field in [
                update_data.name,
                content_dict,
                description_dict,
                update_data.status,
                update_data.published,
                update_data.optimized_for,
            ]
        )
        print(f"💕💕💕💕💕💕💕💕💕💕💕💕 has_updates: {has_updates}")
        if has_updates:
            updated = TemplateVersionRepository.update_version(
                client,
                version_id,
                template_id,
                version_update
            )
            if not updated:
                return None

        # Return the original update_data as confirmation
        return update_data

    @staticmethod
    def delete_version(client: Client, version_id: int, template_id: str) -> dict:
        """Delete a template version. Cannot delete the default version."""
        # Check if version exists and is not default
        version = TemplateVersionRepository.get_version_details(client, version_id, template_id)
        if not version:
            return {"error": "not_found"}

        if version.get("is_default"):
            return {"error": "is_default"}

        success = TemplateVersionRepository.delete_version(client, version_id, template_id)
        if not success:
            return {"error": "delete_failed"}

        return {"success": True}

