from fastapi import Request, HTTPException, status
import logging
from . import router
from services.folder_service import FolderService
from dtos import UpdatePinnedFoldersDTO

logger = logging.getLogger(__name__)

@router.put("/pinned", status_code=status.HTTP_200_OK)
async def update_pinned_folders(
    request: Request,
    data: UpdatePinnedFoldersDTO
):
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} updating pinned folders list")

        result = FolderService.update_pinned_folders(client, user_id, data)

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating pinned folders: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update pinned folders: {str(e)}")
