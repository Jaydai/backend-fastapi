from fastapi import HTTPException, Request, status
import logging

from . import router
from services.template_service import TemplateService
from dtos import TemplateVersionResponseDTO

logger = logging.getLogger(__name__)


@router.get(
    "/{template_id}/versions/{slug}",
    response_model=TemplateVersionResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def get_version_by_slug(
    request: Request,
    template_id: str,
    slug: str
) -> TemplateVersionResponseDTO:
    try:
        client = request.state.supabase_client
        locale = request.headers.get("Accept-Language", "en").split(",")[0][:2]

        version = TemplateService.get_version_by_slug(client, template_id, slug, locale)
        if not version:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template version not found",
            )

        return version

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Error fetching template version %s for template %s: %s",
            slug,
            template_id,
            e,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch template version",
        )
