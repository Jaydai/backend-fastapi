import logging

from fastapi import HTTPException, Request, status

from dtos import CreateFolderDTO, FolderResponseDTO
from services.folder_service import FolderService

from . import router

logger = logging.getLogger(__name__)


@router.post("", response_model=FolderResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_folder(request: Request, data: CreateFolderDTO) -> FolderResponseDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"User {user_id} creating folder: {data.title}")

        folder = FolderService.create_folder(client, user_id, data, locale)

        return folder
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating folder: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create folder: {str(e)}")
