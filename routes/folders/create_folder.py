from fastapi import Request, HTTPException, status
import logging
from . import router
from services.folder_service import FolderService
from dtos import CreateFolderDTO, FolderResponseDTO

logger = logging.getLogger(__name__)

@router.post("", response_model=FolderResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_folder(
    request: Request,
    data: CreateFolderDTO
) -> FolderResponseDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.headers.get("Accept-Language", "en").split(",")[0][:2]

        logger.info(f"User {user_id} creating folder: {data.title}")

        folder = FolderService.create_folder(client, user_id, data, locale)

        return folder
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating folder: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create folder: {str(e)}")
