import logging

from . import router
from services.template_service import TemplateService
from dtos import CreateTemplateVersionDTO

logger = logging.getLogger(__name__)


@router.get("/{template_id}/versions", response_model=list[CreateTemplateVersionDTO], status_code=status.HTTP_200_OK)
async def get_template_versions(
    request: Request,
    template_id: str  # UUID
) -> list[CreateTemplateVersionDTO]:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"User {user_id} fetching versions for template {template_id}")

        versions = TemplateService.get_versions(client, template_id, locale)

        logger.info(f"Returning {len(versions)} versions for template {template_id}")
        return versions

    except Exception as e:
        logger.error(f"Error fetching template versions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch template versions: {str(e)}"
        )
