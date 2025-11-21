from fastapi import Request, Query, HTTPException, status
import logging
from . import router
from services.folder_service import FolderService
from dtos import FolderResponseDTO

logger = logging.getLogger(__name__)

@router.get("", response_model=list[FolderResponseDTO], status_code=status.HTTP_200_OK)
async def get_folders(
    request: Request,
    workspace_type: str | None = Query(None, description="Workspace: user, organization, all"),
    organization_id: str | None = None,
    parent_folder_id: str | None = None
) -> list[FolderResponseDTO]:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.headers.get("Accept-Language", "en").split(",")[0][:2]

        logger.info(f"User {user_id} getting folders with filters: workspace={workspace_type}, org={organization_id}, parent={parent_folder_id}")

        folders = FolderService.get_folders(
            client,
            user_id,
            locale,
            workspace_type,
            organization_id,
            parent_folder_id
        )

        return folders
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting folders: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get folders: {str(e)}")
