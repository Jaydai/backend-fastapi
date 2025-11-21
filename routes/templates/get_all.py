from fastapi import HTTPException, Request, Query, status
import logging

from . import router
from services.template_service import TemplateService
from dtos import TemplateListItemDTO

logger = logging.getLogger(__name__)


@router.get("", response_model=list[TemplateListItemDTO], status_code=status.HTTP_200_OK)
async def get_all_templates(
    request: Request,
    workspace_type: str | None = Query(None, description="Workspace: user, organization"),
    organization_id: str | None = None,
    folder_id: int | None = None,
    tags: str | None = Query(None, description="Comma-separated tags"),
    published: bool | None = None,
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0)
) -> list[TemplateListItemDTO]:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.headers.get("Accept-Language", "en").split(",")[0][:2]

        logger.info(f"User {user_id} fetching templates with workspace_type={workspace_type}")

        tag_list = [t.strip() for t in tags.split(",")] if tags else None

        templates = TemplateService.get_templates(
            client,
            user_id,
            locale,
            workspace_type,
            organization_id,
            folder_id,
            tag_list,
            published,
            limit,
            offset
        )

        logger.info(f"Returning {len(templates)} templates for user {user_id}")
        return templates

    except Exception as e:
        logger.error(f"Error fetching templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch templates: {str(e)}"
        )
