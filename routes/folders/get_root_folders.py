from fastapi import Request, Query, HTTPException, status
import logging
from . import router
from services.folder_service import FolderService
from dtos import FolderResponseDTO

logger = logging.getLogger(__name__)

@router.get("/root", response_model=list[FolderResponseDTO], status_code=status.HTTP_200_OK)
async def get_root_folders(
    request: Request,
    workspace_type: str | None = Query(None, description="Workspace: user, organization"),
    organization_id: str | None = None
) -> list[FolderResponseDTO]:
    """
    Get only root-level folders (without nested items).
    More efficient than get_root_items for initial panel loading.
    """
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.headers.get("Accept-Language", "en").split(",")[0][:2]

        logger.info(f"User {user_id} getting root folders (workspace_type={workspace_type})")

        folders = FolderService.get_folders(
            client,
            user_id,
            locale,
            workspace_type,
            organization_id,
            "root"
        )

        return folders
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting root folders: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get root folders: {str(e)}")
