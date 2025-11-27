import logging

from fastapi import HTTPException, Request, status

from dtos import UpdatePinnedBlocksDTO
from services.block_service import BlockService

from . import router

logger = logging.getLogger(__name__)


@router.put("/pinned", status_code=status.HTTP_200_OK)
async def update_pinned_blocks(request: Request, data: UpdatePinnedBlocksDTO):
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} updating pinned blocks list")

        result = BlockService.update_pinned_blocks(client, user_id, data)

        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating pinned blocks: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to update pinned blocks: {str(e)}"
        )
