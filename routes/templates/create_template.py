from fastapi import HTTPException, Request, status
import logging

from . import router
from services.template_service import TemplateService
from dtos import CreateTemplateDTO, TemplateResponseDTO

logger = logging.getLogger(__name__)


@router.post("", response_model=TemplateResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_template(
    request: Request,
    data: CreateTemplateDTO
) -> TemplateResponseDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.headers.get("Accept-Language", "en").split(",")[0][:2]

        logger.info(f"User {user_id} creating template: {data.title}")

        template = TemplateService.create_template(client, user_id, data, locale)

        logger.info(f"Template {template.id} created successfully")
        return template

    except Exception as e:
        logger.error(f"Error creating template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create template: {str(e)}"
        )
