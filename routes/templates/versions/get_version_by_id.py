import logging

from fastapi import HTTPException, Request, status

from dtos import TemplateVersionDTO
from services import TemplateVersionService

from . import router

logger = logging.getLogger(__name__)


@router.get("/versions/{version_id}", response_model=TemplateVersionDTO, status_code=status.HTTP_200_OK)
async def get_version_by_id(request: Request, version_id: int) -> TemplateVersionDTO:
    """Get a specific template version by its ID"""
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"User {user_id} fetching version {version_id}")

        version = TemplateVersionService.get_version_by_id(client, version_id, locale)

        if not version:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Version {version_id} not found")

        logger.info(f"Version {version_id} fetched successfully")
        return version

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching version: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch version: {str(e)}"
        )
