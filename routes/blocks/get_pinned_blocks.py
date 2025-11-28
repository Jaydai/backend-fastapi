import logging

from fastapi import HTTPException, Request, status

from dtos import BlockResponseDTO
from services.block_service import BlockService

from . import router

logger = logging.getLogger(__name__)


@router.get("/pinned", response_model=list[BlockResponseDTO], status_code=status.HTTP_200_OK)
async def get_pinned_blocks(request: Request) -> list[BlockResponseDTO]:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"User {user_id} getting pinned blocks")

        blocks = BlockService.get_pinned_blocks(client, user_id, locale)

        return blocks
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting pinned blocks: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get pinned blocks: {str(e)}")
