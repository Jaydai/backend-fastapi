from fastapi import HTTPException, Request, status
import logging

from . import router
from services.template_service import TemplateService
from dtos import UsageResponseDTO

logger = logging.getLogger(__name__)


@router.post("/{template_id}/usages", response_model=UsageResponseDTO, status_code=status.HTTP_201_CREATED)
async def track_template_usage(
    request: Request,
    template_id: str  # UUID
) -> UsageResponseDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} tracking usage for template {template_id}")

        usage = TemplateService.increment_usage(client, template_id)

        logger.info(f"Template {template_id} usage count: {usage.usage_count}")
        return usage

    except Exception as e:
        logger.error(f"Error tracking template usage: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to track template usage: {str(e)}"
        )
