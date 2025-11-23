from supabase import Client
from dtos import CreateTemplateDTO, TemplateResponseDTO
from repositories.template_repository import TemplateRepository
from mappers.template_mapper import TemplateMapper
from services.templates import get_by_id

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
            data.tags,
            workspace_type
        )

        try:
            version = TemplateRepository.create_version(
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

        return get_by_id(client, template.id, locale)
