from fastapi import Request, HTTPException, status
import logging
from . import router
from services.folder_service import FolderService
from dtos import FolderResponseDTO

logger = logging.getLogger(__name__)

@router.get("/pinned", response_model=list[FolderResponseDTO], status_code=status.HTTP_200_OK)
async def get_pinned_folders(
    request: Request
) -> list[FolderResponseDTO]:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.headers.get("Accept-Language", "en").split(",")[0][:2]

        logger.info(f"User {user_id} getting pinned folders")

        folders = FolderService.get_pinned_folders(client, user_id, locale)

        return folders
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting pinned folders: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get pinned folders: {str(e)}")
