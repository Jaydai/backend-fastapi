from domains.entities import Template, TemplateVersion, TemplateComment, TemplateCommentAuthor
from dtos import (
    TemplateListItemDTO,
    TemplateResponseDTO,
    TemplateVersionResponseDTO,
    TemplateCommentDTO,
    TemplateCommentAuthorDTO,
)

class TemplateMapper:
    @staticmethod
    def localize_string(value: dict[str, str] | str | None, locale: str = "en") -> str:
        # TODO need to use an appropriate service
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            return value.get(locale) or value.get("en") or list(value.values())[0] if value else ""
        return ""

    @staticmethod
    def ensure_localized_dict(value: str | None, locale: str = "en") -> dict[str, str]:
        # TODO need to use an appropriate service
        if value is None:
            return {locale: ""}
        return {locale: value}

    @staticmethod
    def entity_to_list_item_dto(template: Template, locale: str = "en") -> TemplateListItemDTO:
        return TemplateListItemDTO(
            id=template.id,
            title=TemplateMapper.localize_string(template.title, locale),
            description=TemplateMapper.localize_string(template.description, locale) if template.description else None,
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
        versions: list[TemplateVersion],
        comments: list[TemplateComment] | None = None,
        locale: str = "en"
    ) -> TemplateResponseDTO:
        version_dtos = [TemplateMapper.version_entity_to_dto(v, locale) for v in versions]

        current_version = None
        current_content = ""

        if template.current_version_id:
            for v in versions:
                if v.id == template.current_version_id:
                    current_version = TemplateMapper.version_entity_to_dto(v, locale)
                    current_content = current_version.content
                    break

        if not current_version and version_dtos:
            current_version = version_dtos[0]
            current_content = current_version.content

        comment_dtos = [TemplateMapper.comment_entity_to_dto(c) for c in comments] if comments else []

        return TemplateResponseDTO(
            id=template.id,
            title=TemplateMapper.localize_string(template.title, locale),
            description=TemplateMapper.localize_string(template.description, locale) if template.description else None,
            content=current_content,
            folder_id=template.folder_id,
            organization_id=template.organization_id,
            user_id=template.user_id,
            workspace_type=template.workspace_type,
            created_at=template.created_at,
            updated_at=template.updated_at,
            tags=template.tags,
            usage_count=template.usage_count,
            last_used_at=template.last_used_at,
            current_version_id=template.current_version_id,
            is_free=template.is_free,
            is_published=template.is_published,
            versions=version_dtos,
            current_version=current_version,
            comments=comment_dtos
        )

    @staticmethod
    def version_entity_to_dto(version: TemplateVersion, locale: str = "en") -> TemplateVersionResponseDTO:
        return TemplateVersionResponseDTO(
            id=version.id,
            template_id=version.template_id,
            name=version.name,
            content=TemplateMapper.localize_string(version.content, locale),
            change_notes=TemplateMapper.localize_string(version.change_notes, locale) if version.change_notes else None,
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
