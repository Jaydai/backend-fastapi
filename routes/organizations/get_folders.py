import logging

from fastapi import HTTPException, Request, status

from domains.enums import PermissionEnum
from dtos import FolderTitleResponseDTO
from routes.dependencies import require_permission_in_organization
from services import FolderService

from . import router

logger = logging.getLogger(__name__)


@router.get("/{organization_id}/folders", response_model=list[FolderTitleResponseDTO])
@require_permission_in_organization(PermissionEnum.ORGANIZATION_READ)
async def get_organization_folders(
    request: Request,
    organization_id: str,
) -> list[FolderTitleResponseDTO]:
    locale = request.state.locale
    try:
        # Fetch all folders for the organization (minimal data for tree building)
        folders = FolderService.get_folders_titles(
            client=request.state.supabase_client,
            locale=locale,
            user_id=None,
            organization_id=organization_id,
            parent_folder_id=None,  # Not used anymore, we fetch all
            limit=1000,
            offset=0,
        )
        return folders

    except Exception as e:
        logger.error(f"Error fetching folders for organization {organization_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch folders: {str(e)}"
        )
