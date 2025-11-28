import logging

from fastapi import HTTPException, Request, status

from dtos import FolderResponseDTO
from services.folder_service import FolderService

from . import router

logger = logging.getLogger(__name__)


@router.get("/pinned", response_model=list[FolderResponseDTO], status_code=status.HTTP_200_OK)
async def get_pinned_folder_ids(request: Request) -> list[FolderResponseDTO]:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"User {user_id} getting pinned folders")

        folders = FolderService.get_pinned_folder_ids(client, user_id, locale)

        return folders
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting pinned folders: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get pinned folders: {str(e)}")
