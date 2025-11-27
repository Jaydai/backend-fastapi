from fastapi import HTTPException, Request, status
import logging

from . import router
from services.template_service import TemplateService
from dtos import UpdateTemplateDTO, TemplateResponseDTO

logger = logging.getLogger(__name__)


@router.patch("/{template_id}", response_model=TemplateResponseDTO, status_code=status.HTTP_200_OK)
async def update_template(
    request: Request,
    template_id: str,  # UUID
    data: UpdateTemplateDTO
) -> TemplateResponseDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"User {user_id} updating template {template_id}")

        template = TemplateService.update_template(client, template_id, data, locale)

        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template {template_id} not found"
            )

        logger.info(f"Template {template_id} updated successfully")
        return template

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update template: {str(e)}"
        )
