from fastapi import Request, HTTPException, status
import logging
from . import router
from services.folder_service import FolderService
from dtos import FolderResponseDTO

logger = logging.getLogger(__name__)

@router.get("/{folder_id}", response_model=FolderResponseDTO, status_code=status.HTTP_200_OK)
async def get_folder(
    request: Request,
    folder_id: str
) -> FolderResponseDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"User {user_id} getting folder {folder_id}")

        folder = FolderService.get_folder_by_id(client, folder_id, locale)

        if not folder:
            raise HTTPException(status_code=404, detail="Folder not found")

        return folder
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting folder: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get folder: {str(e)}")
