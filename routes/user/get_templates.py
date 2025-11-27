from fastapi import HTTPException, Request, Query, status
import logging
from . import router
from services import TemplateService
from dtos import TemplateTitleResponseDTO


logger = logging.getLogger(__name__)


@router.get(
    "/templates",
    response_model=list[TemplateTitleResponseDTO]
)
async def get_user_templates(
    request: Request,
) -> list[TemplateTitleResponseDTO]:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        templates = TemplateService.get_templates_titles(
            client=client,
            locale=locale,
            user_id=user_id,
            organization_id=None,
            folder_id=None,
            limit=1000,
            offset=0
        )
        return templates

    except Exception as e:
        logger.error(f"Error fetching user templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user templates: {str(e)}"
        )
