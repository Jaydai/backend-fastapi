import logging

from . import router
from services.template_version_service import TemplateVersionService
from dtos import CreateVersionDTO, CreateTemplateVersionDTO

logger = logging.getLogger(__name__)


@router.post("/{template_id}/versions", response_model=CreateTemplateVersionDTO, status_code=status.HTTP_201_CREATED)
async def create_template_version(
    request: Request,
    template_id: str,
    data: CreateVersionDTO
) -> CreateTemplateVersionDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"User {user_id} creating version for template {template_id}")

        version = TemplateVersionService.create_version(client, template_id, user_id, data, locale)

        if not version:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template or source version not found")

        logger.info(f"Version {version.id} created successfully for template {template_id}")
        return version

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating template version: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create template version: {str(e)}"
        )
