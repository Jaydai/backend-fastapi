from fastapi import HTTPException, Request, Query, status
import logging

from . import router
from services import FolderService
from dtos import FolderTitleResponseDTO
from routes.dependencies import require_permission_in_organization
from domains.enums import PermissionEnum

logger = logging.getLogger(__name__)


@router.get(
    "/{organization_id}/folders",
    response_model=list[FolderTitleResponseDTO]
)
@require_permission_in_organization(PermissionEnum.ORGANIZATION_READ)
async def get_organization_folders(
    request: Request,
    organization_id: str,
    parent_folder_id: str | None = Query(None, description="Parent folder ID to filter folders. Empty string for root only."),
    locale: str = Query("en", description="Locale for localization")
) -> list[FolderTitleResponseDTO]:
    try:
        folders = FolderService.get_folders_titles(
            client=request.state.supabase_client,
            locale=locale,
            user_id=None,
            organization_id=organization_id,
            parent_folder_id=parent_folder_id,
            limit=1000,
            offset=0
        )
        return folders

    except Exception as e:
        logger.error(f"Error fetching templates for organization {organization_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch templates: {str(e)}"
        )
