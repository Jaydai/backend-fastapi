from fastapi import HTTPException, Request, Query, status
import logging
from . import router
from services import FolderService
from dtos import FolderTitleResponseDTO


logger = logging.getLogger(__name__)


@router.get(
    "/folders",
    response_model=list[FolderTitleResponseDTO]
)
async def get_user_folders(
    request: Request,
) -> list[FolderTitleResponseDTO]:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        folders = FolderService.get_folders_titles(
            client=client,
            locale=locale,
            user_id=user_id,
            organization_id=None,
            parent_folder_id=None,
            limit=1000,
            offset=0
        )
        return folders

    except Exception as e:
        logger.error(f"Error fetching user folders: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user folders: {str(e)}"
        )
