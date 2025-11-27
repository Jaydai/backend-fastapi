from domains.entities import Template, TemplateVersion, TemplateComment, TemplateCommentAuthor, VersionSummary
from dtos import (
    TemplateListItemDTO,
    TemplateResponseDTO,
    TemplateVersionResponseDTO,
    TemplateCommentDTO,
    TemplateCommentAuthorDTO,
)
from services.locale_service import LocaleService

class TemplateMapper:

    @staticmethod
    def entity_to_list_item_dto(template: Template, locale: str = LocaleService.DEFAULT_LOCALE) -> TemplateListItemDTO:
        return TemplateListItemDTO(
            id=template.id,
            title=LocaleService.localize_string(template.title, locale),
            description=LocaleService.localize_string(template.description, locale) if template.description else None,
            folder_id=template.folder_id,
            organization_id=template.organization_id,
            user_id=template.user_id,
            workspace_type=template.workspace_type,
            created_at=template.created_at,
            updated_at=template.updated_at,
            tags=template.tags,
            usage_count=template.usage_count,
            current_version_id=template.current_version_id,
            is_free=template.is_free,
            is_published=template.is_published
        )

    @staticmethod
    def entity_to_response_dto(
        template: Template,
        versions_summary: list[VersionSummary],
        locale: str = LocaleService.DEFAULT_LOCALE
    ) -> TemplateResponseDTO:
        version_dtos = [VersionSummary(v.id, LocaleService.localize_string(v.name, locale), v.slug, v.is_current) for v in versions_summary]

        return TemplateResponseDTO(
            id=template.id,
            title=LocaleService.localize_string(template.title, locale),
            description=LocaleService.localize_string(template.description, locale) if template.description else None,
            folder_id=template.folder_id,
            organization_id=template.organization_id,
            user_id=template.user_id,
            created_at=template.created_at,
            updated_at=template.updated_at,
            last_used_at=template.last_used_at,
            usage_count=template.usage_count,
            current_version_id=template.current_version_id,
            is_published=template.is_published,
            versions=version_dtos
            )

    @staticmethod
    def version_entity_to_dto(version: TemplateVersion, locale: str = LocaleService.DEFAULT_LOCALE) -> TemplateVersionResponseDTO:
        return TemplateVersionResponseDTO(
            id=version.id,
            template_id=version.template_id,
            name=version.name,
            content=LocaleService.localize_string(version.content, locale),
            change_notes=LocaleService.localize_string(version.change_notes, locale) if version.change_notes else None,
            author_id=version.author_id,
            created_at=version.created_at,
            updated_at=version.updated_at,
            status=version.status,
            is_current=version.is_current,
            is_published=version.is_published,
            usage_count=version.usage_count,
            parent_version_id=version.parent_version_id,
            optimized_for=version.optimized_for
        )

    @staticmethod
    def comment_author_entity_to_dto(author: TemplateCommentAuthor) -> TemplateCommentAuthorDTO:
        return TemplateCommentAuthorDTO(
            id=author.id,
            name=author.name,
            avatar=author.avatar
        )

    @staticmethod
    def comment_entity_to_dto(comment: TemplateComment) -> TemplateCommentDTO:
        replies_dtos = [TemplateMapper.comment_entity_to_dto(reply) for reply in comment.replies]

        return TemplateCommentDTO(
            id=comment.id,
            text=comment.text,
            parent_comment_id=comment.parent_id,
            version_id=comment.version_id,
            created_at=comment.created_at,
            author=TemplateMapper.comment_author_entity_to_dto(comment.author),
            mentions=comment.mentions,
            replies=replies_dtos
        )
