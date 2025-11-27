from fastapi import HTTPException, Request, status
import logging

from . import router
from services.template_service import TemplateService
from dtos import TemplateResponseDTO

logger = logging.getLogger(__name__)


@router.get("/{template_id}", response_model=TemplateResponseDTO, status_code=status.HTTP_200_OK)
async def get_template_by_id(
    request: Request,
    template_id: str,
) -> TemplateResponseDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale
        published = request.query_params.get("published", None)

        logger.info(f"User {user_id} fetching template {template_id}")

        template = TemplateService.get_template_by_id(client, template_id, published, locale)

        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template {template_id} not found"
            )

        logger.info(f"Template {template_id} fetched successfully")
        return template

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch template: {str(e)}"
        )
