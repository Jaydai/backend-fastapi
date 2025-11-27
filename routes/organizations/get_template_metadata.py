from fastapi import HTTPException, Request, Query, status
import logging

from . import router
from services.templates import get_template_metadata as service_get_template_metadata
from dtos import TemplateMetadataDTO
from routes.dependencies import require_permission_in_organization
from domains.enums import PermissionEnum

logger = logging.getLogger(__name__)


@router.get(
    "/{organization_id}/templates/{template_id}/metadata",
    response_model=TemplateMetadataDTO
)
@require_permission_in_organization(PermissionEnum.ORGANIZATION_READ)
async def get_organization_template_metadata(
    request: Request,
    organization_id: str,
    template_id: str,
) -> TemplateMetadataDTO:
    """
    Get template metadata with version summaries (no content).

    This endpoint is optimized for the initial template detail page load:
    - Returns template metadata without content
    - Includes all version summaries (id, name, slug, is_current)
    - Excludes comments (fetched separately)

    Use this for the first render, then fetch specific version content
    using the version slug endpoint.
    """
    locale = request.state.locale
    try:
        metadata = service_get_template_metadata(
            client=request.state.supabase_client,
            locale=locale,
            template_id=template_id
        )

        if not metadata:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template {template_id} not found"
            )

        # Verify template belongs to this organization
        if metadata.organization_id != organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Template does not belong to this organization"
            )

        return metadata

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching template metadata {template_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch template metadata: {str(e)}"
        )
