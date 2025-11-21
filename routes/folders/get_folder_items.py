from fastapi import Request, HTTPException, status
import logging
from . import router
from services.folder_service import FolderService
from dtos import FolderWithItemsDTO

logger = logging.getLogger(__name__)

@router.get("/{folder_id}/items", response_model=FolderWithItemsDTO, status_code=status.HTTP_200_OK)
async def get_folder_items(
    request: Request,
    folder_id: str
) -> FolderWithItemsDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.headers.get("Accept-Language", "en").split(",")[0][:2]

        logger.info(f"User {user_id} getting items for folder {folder_id}")

        items = FolderService.get_folder_items(client, folder_id, locale)

        return items
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting folder items: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get folder items: {str(e)}")
