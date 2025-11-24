import logging

from fastapi import HTTPException, Request, status

from services.folder_service import FolderService

from . import router

logger = logging.getLogger(__name__)


@router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_folder(request: Request, folder_id: str):
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} deleting folder {folder_id}")

        success = FolderService.delete_folder(client, folder_id)

        if not success:
            raise HTTPException(status_code=404, detail="Folder not found")

        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting folder: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete folder: {str(e)}")
