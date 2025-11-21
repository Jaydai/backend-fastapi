from fastapi import Request, Query, HTTPException, status
import logging
from . import router
from services.folder_service import FolderService
from dtos import FolderTitleResponseDTO

logger = logging.getLogger(__name__)

@router.get("", response_model=list[FolderTitleResponseDTO], status_code=status.HTTP_200_OK)
async def get_folders(
    request: Request,
    organization_id: str | None = None,
    parent_folder_ids: str | None = Query(None, description="Comma-separated parent folder IDs to filter. Empty for root only."),
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0)
) -> list[FolderTitleResponseDTO]:

    try:
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"Fetching folder titles with parent_folder_ids={parent_folder_ids}, org={organization_id}")

        # Parse parent_folder_ids
        parent_id_list: list[str] | None = None
        if parent_folder_ids is not None:
            if parent_folder_ids == "":
                parent_id_list = []
            else:
                parent_id_list = [pid.strip() for pid in parent_folder_ids.split(",") if pid.strip()]

        folders = FolderService.get_folders_titles(
            client,
            locale,
            organization_id,
            parent_id_list,
            limit,
            offset
        )

        logger.info(f"Returning {len(folders)} folder titles")
        return folders
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting folder titles: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get folder titles: {str(e)}")
