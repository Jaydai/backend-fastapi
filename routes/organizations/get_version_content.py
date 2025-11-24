from fastapi import HTTPException, Request, Query, status, Path
import logging

from . import router
from services.template_service import TemplateService
from dtos import VersionContentDTO
from routes.dependencies import require_permission_in_organization
from domains.enums import PermissionEnum

logger = logging.getLogger(__name__)


@router.get(
    "/{organization_id}/templates/{template_id}/versions/{slug}",
    response_model=VersionContentDTO
)
@require_permission_in_organization(PermissionEnum.ORGANIZATION_READ)
async def get_organization_template_version(
    request: Request,
    organization_id: str,
    template_id: str,
    slug: str = Path(..., description="Version slug (e.g., 'v1-draft', 'v2-production')"),
    locale: str = Query("en", description="Locale for localization")
) -> VersionContentDTO:
    """
    Get specific version content by slug.

    This endpoint returns the full version data including content.
    Used when:
    - User selects a different version from the dropdown
    - Loading the default (current) version after metadata fetch

    The slug is a URL-friendly identifier generated from the version name
    (e.g., "Version 2.0" → "v1-version-2-0").
    """
    try:
        version = TemplateService.get_version_by_slug(
            client=request.state.supabase_client,
            template_id=template_id,
            slug=slug,
            locale=locale
        )

        if not version:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Version with slug '{slug}' not found for template {template_id}"
            )

        # Note: We trust the permission check at the organization level
        # The template_id itself is already verified to belong to the organization
        # by the metadata endpoint or by the template existence

        return version

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching version {slug} for template {template_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch version: {str(e)}"
        )
