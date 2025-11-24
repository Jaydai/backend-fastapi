import logging
from . import router
from services.folder_service import FolderService
from dtos import FolderTitleResponseDTO

logger = logging.getLogger(__name__)

@router.get("", response_model=list[FolderTitleResponseDTO], status_code=status.HTTP_200_OK)
async def get_folders(
    request: Request,
    workspace_type: str | None = Query(None, description="Workspace: user, organization, all"),
    organization_id: str | None = None,
    parent_folder_id: str | None = None,
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0)
) -> list[FolderTitleResponseDTO]:
    try:
        client = request.state.supabase_client
        locale = request.state.locale
        user_id = request.state.user_id

        logger.info(f"User {user_id} fetching folders with workspace={workspace_type}, org={organization_id}, parent={parent_folder_id}")

        folders = FolderService.get_folders_titles(
            client,
            user_id,
            locale,
            workspace_type,
            organization_id,
            parent_folder_id,
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
