import logging

from fastapi import HTTPException, Request, status

from services.folder_service import FolderService

from . import router

logger = logging.getLogger(__name__)


@router.patch("/{folder_id}/pin", status_code=status.HTTP_200_OK)
async def toggle_pin_folder(request: Request, folder_id: str, pinned: bool):
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} {'pinning' if pinned else 'unpinning'} folder {folder_id}")

        if pinned:
            result = FolderService.pin_folder(client, user_id, folder_id)
        else:
            result = FolderService.unpin_folder(client, user_id, folder_id)

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error toggling pin folder: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to toggle pin folder: {str(e)}")
