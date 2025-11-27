import logging

from fastapi import HTTPException, Request, status

from dtos import TemplateCountsResponseDTO
from services.template_service import TemplateService

from . import router

logger = logging.getLogger(__name__)


@router.get("/template_counts", response_model=TemplateCountsResponseDTO)
async def get_templates_counts(
    request: Request,
) -> TemplateCountsResponseDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        templates_counts = TemplateService.get_templates_counts(client, user_id)
        return templates_counts

    except Exception as e:
        logger.error(f"Error getting templates counts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get templates counts: {str(e)}"
        )
