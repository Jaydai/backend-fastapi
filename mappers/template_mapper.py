from domains.entities import Template, TemplateComment, TemplateCommentAuthor, TemplateVersionUpdate, VersionDetails, VersionSummary
from dtos import (
    TemplateCommentAuthorDTO,
    TemplateCommentDTO,
    TemplateListItemDTO,
    TemplateResponseDTO,
    TemplateVersionDTO,
    UpdateTemplateVersionDTO,
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
            published=template.published,
        )

    @staticmethod
    def entity_to_response_dto(
        template: Template, versions_summary: list[VersionSummary], locale: str = LocaleService.DEFAULT_LOCALE
    ) -> TemplateResponseDTO:
        version_dtos = [
            VersionSummary(
                id=v.id,
                name=LocaleService.localize_string(v.name, locale),
                is_default=v.is_default,
                published=v.published,
            )
            for v in versions_summary
        ]

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
            published=template.published,
            versions=version_dtos,
        )

    @staticmethod
    def version_entity_to_content_dto(
        version: VersionDetails, locale: str = LocaleService.DEFAULT_LOCALE
    ) -> TemplateVersionDTO:
        """Map version entity to TemplateVersionDTO for fetching version content"""
        return TemplateVersionDTO(
            id=version.id,
            content=LocaleService.localize_string(version.content, locale),
            status=version.status,
            published=version.published,
            optimized_for=version.optimized_for,
            )

    @staticmethod
    def update_version_entity_to_dto(
        version: TemplateVersionUpdate, locale: str = LocaleService.DEFAULT_LOCALE
    ) -> UpdateTemplateVersionDTO:
        return UpdateTemplateVersionDTO(
            content=LocaleService.localize_string(version.content if getattr(version, "content", None) is not None else {locale: ""}, locale)
                if getattr(version, "content", None) is not None else None,
            description=LocaleService.localize_string(version.description if getattr(version, "description", None) is not None else {locale: ""}, locale)
                if getattr(version, "description", None) is not None else None,
            status=getattr(version, "status", None),
            is_default=getattr(version, "is_default", None),
            published=getattr(version, "published", None),
            optimized_for=getattr(version, "optimized_for", None),
        )


    @staticmethod
    def comment_author_entity_to_dto(author: TemplateCommentAuthor) -> TemplateCommentAuthorDTO:
        return TemplateCommentAuthorDTO(id=author.id, name=author.name, avatar=author.avatar)

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
            replies=replies_dtos,
        )
