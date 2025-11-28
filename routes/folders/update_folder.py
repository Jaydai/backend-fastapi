import logging

from fastapi import HTTPException, Request, status

from dtos import FolderResponseDTO, UpdateFolderDTO
from services.folder_service import FolderService

from . import router

logger = logging.getLogger(__name__)


@router.patch("/{folder_id}", response_model=FolderResponseDTO, status_code=status.HTTP_200_OK)
async def update_folder(request: Request, folder_id: str, data: UpdateFolderDTO) -> FolderResponseDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"User {user_id} updating folder {folder_id}")

        folder = FolderService.update_folder(client, folder_id, data, locale)

        if not folder:
            raise HTTPException(status_code=404, detail="Folder not found")

        return folder
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating folder: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update folder: {str(e)}")
