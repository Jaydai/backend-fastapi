import logging

from fastapi import HTTPException, Query, Request, status

from dtos import TemplateListItemDTO
from services.template_service import TemplateService

from . import router

logger = logging.getLogger(__name__)


@router.get("/search", response_model=list[TemplateListItemDTO], status_code=status.HTTP_200_OK)
async def search_templates(
    request: Request,
    q: str = Query(..., min_length=2, description="Search query"),
    tags: str | None = Query(None, description="Comma-separated tags"),
    include_public: bool = True,
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
) -> list[TemplateListItemDTO]:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"User {user_id} searching templates with query: {q}")

        tag_list = [t.strip() for t in tags.split(",")] if tags else None

        templates = TemplateService.search_templates(
            client, user_id, q, locale, tag_list, include_public, limit, offset
        )

        logger.info(f"Returning {len(templates)} search results")
        return templates

    except Exception as e:
        logger.error(f"Error searching templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to search templates: {str(e)}"
        )
