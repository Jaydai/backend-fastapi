from supabase import Client
from dtos import UpdateTemplateDTO, TemplateResponseDTO
from repositories.template_repository import TemplateRepository
from mappers.template_mapper import TemplateMapper
from services.templates import get_by_id

def update_template(
        client: Client,
        template_id: str,
        data: UpdateTemplateDTO,
        locale: str = "en"
    ) -> TemplateResponseDTO | None:
        template = TemplateRepository.get_by_id(client, template_id)
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

        return get_by_id(client, template_id, locale)
