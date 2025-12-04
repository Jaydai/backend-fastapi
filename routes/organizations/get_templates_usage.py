import logging

from fastapi import HTTPException, Request, status

from domains.enums import PermissionEnum
from dtos import TemplateUsageDTO
from repositories import TemplateRepository
from routes.dependencies import require_permission_in_organization
from services.locale_service import LocaleService

from . import router

logger = logging.getLogger(__name__)


@router.get("/{organization_id}/templates/usage", response_model=list[TemplateUsageDTO])
@require_permission_in_organization(PermissionEnum.ORGANIZATION_READ)
async def get_organization_templates_usage(
    request: Request,
    organization_id: str,
    published: bool | None = None,
) -> list[TemplateUsageDTO]:
    """Get organization templates with usage statistics for dashboards"""
    locale = request.state.locale
    try:
        templates = TemplateRepository.get_templates_with_usage(
            request.state.supabase_client,
            organization_id=organization_id,
            published=published,
            limit=1000,
            offset=0,
        )

        return [
            TemplateUsageDTO(
                id=t.id,
                title=LocaleService.localize_string(t.title, locale),
                folder_id=t.folder_id,
                usage_count=t.usage_count,
                last_used_at=t.last_used_at,
                created_at=t.created_at,
            )
            for t in templates
        ]

    except Exception as e:
        logger.error(f"Error fetching template usage for organization {organization_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch template usage: {str(e)}"
        )
