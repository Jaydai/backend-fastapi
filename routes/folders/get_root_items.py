from fastapi import Request, Query, HTTPException, status
import logging
from . import router
from services.folder_service import FolderService
from dtos import FolderWithItemsDTO

logger = logging.getLogger(__name__)

@router.get("/root/items", response_model=FolderWithItemsDTO, status_code=status.HTTP_200_OK)
async def get_root_items(
    request: Request,
    workspace_type: str | None = Query(None, description="Workspace: user, organization, all"),
    organization_id: str | None = None
) -> FolderWithItemsDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.headers.get("Accept-Language", "en").split(",")[0][:2]

        logger.info(f"User {user_id} getting root items")

        items = FolderService.get_root_items(
            client,
            user_id,
            locale,
            workspace_type,
            organization_id
        )

        return items
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting root items: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get root items: {str(e)}")
