from fastapi import HTTPException, Request, Query, status
import logging

from . import router
from services import FolderService
from dtos import FolderResponseDTO
from routes.dependencies import require_permission_in_organization
from domains.enums import PermissionEnum

logger = logging.getLogger(__name__)


@router.get(
    "/{organization_id}/folders",
    response_model=list[FolderResponseDTO]
)
@require_permission_in_organization(PermissionEnum.ORGANIZATION_READ)
async def get_organization_folders(
    request: Request,
    organization_id: str,
    parent_folder_ids: str | None = Query(None, description="Comma-separated parent folder IDs to filter. Empty string for root only."),
    locale: str = Query("en", description="Locale for localization")
) -> list[FolderResponseDTO]:
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} fetching folders for organization {organization_id} with parent_folder_ids={parent_folder_ids}")

        # Parse parent_folder_ids parameter
        parent_id_list: list[str] | None = None
        if parent_folder_ids is not None:
            if parent_folder_ids == "":
                # Empty string means root only (parent_folder_id = null)
                parent_id_list = []
            else:
                # Parse comma-separated IDs
                parent_id_list = [pid.strip() for pid in parent_folder_ids.split(",") if pid.strip()]

        folders = FolderService.get_folders(
            request.state.supabase_client,
            user_id,
            locale,
            workspace_type=None,
            organization_id=organization_id,
            parent_folder_id=None  # We'll filter below
        )

        # Filter by parent_folder_ids if specified
        if parent_id_list is not None:
            if len(parent_id_list) == 0:
                # Root only
                folders = [f for f in folders if f.parent_folder_id is None]
            else:
                # Filter by specific parent folder IDs
                folders = [f for f in folders if f.parent_folder_id in parent_id_list]

        logger.info(
            f"Returning {len(folders)} folders for organization {organization_id} "
            f"to user {user_id}"
        )

        return folders

    except Exception as e:
        logger.error(f"Error fetching folders for organization {organization_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch folders: {str(e)}"
        )
