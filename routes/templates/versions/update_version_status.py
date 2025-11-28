import logging

from fastapi import HTTPException, Request, status

from dtos import TemplateVersionContentDTO, UpdateVersionStatusDTO
from services.template_version_service import TemplateVersionService

from . import router

logger = logging.getLogger(__name__)


@router.patch("/versions/{version_id}/status", response_model=TemplateVersionContentDTO, status_code=status.HTTP_200_OK)
async def update_version_status(
    request: Request, version_id: int, data: UpdateVersionStatusDTO
) -> TemplateVersionContentDTO:
    """Update version status fields (published, status, is_current)"""
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"User {user_id} updating version {version_id} status")

        version = TemplateVersionService.update_version_status(
            client,
            version_id,
            data.template_id,
            published=data.published,
            status=data.status,
            is_current=data.is_current,
            locale=locale,
        )

        if not version:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Version {version_id} not found")

        logger.info(f"Version {version_id} status updated successfully")
        return version

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating version status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update version status: {str(e)}"
        )
