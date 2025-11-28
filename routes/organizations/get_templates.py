import logging

from fastapi import HTTPException, Request, status

from domains.enums import PermissionEnum
from dtos import TemplateTitleResponseDTO
from routes.dependencies import require_permission_in_organization
from services import TemplateService

from . import router

logger = logging.getLogger(__name__)


@router.get("/{organization_id}/templates", response_model=list[TemplateTitleResponseDTO])
@require_permission_in_organization(PermissionEnum.ORGANIZATION_READ)
async def get_organization_templates(
    request: Request,
    organization_id: str,
    published: bool | None = None,
) -> list[TemplateTitleResponseDTO]:
    locale = request.state.locale
    try:
        # Fetch all templates for the organization (minimal data for tree building)
        templates = TemplateService.get_templates_titles(
            request.state.supabase_client,
            locale=locale,
            user_id=None,
            organization_id=organization_id,
            folder_id=None,  # Not used anymore, we fetch all
            published=published,
            limit=1000,
            offset=0,
        )
        return templates

    except Exception as e:
        logger.error(f"Error fetching templates for organization {organization_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch templates: {str(e)}"
        )
