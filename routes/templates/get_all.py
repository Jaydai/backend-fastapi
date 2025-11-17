from fastapi import HTTPException, Request
import logging

from . import router
from services import TemplateService
from dtos import TemplateTitleResponseDTO

logger = logging.getLogger(__name__)


@router.get("")
async def get_all_accessible_templates(
    request: Request
) -> list[TemplateTitleResponseDTO]:
    try:
        user_id = request.state.user_id  # Injected by middleware
        logger.info(f"User {user_id} fetching accessible templates")
        
        # RLS will automatically filter based on user permissions
        templates = TemplateService.get_all_templates_title()
        
        logger.info(f"Returning {len(templates)} templates for user {user_id}")
        return templates
    
    except Exception as e:
        logger.error(f"Error fetching templates for user: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch templates: {str(e)}"
        )
