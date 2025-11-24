import logging

from fastapi import HTTPException, Request, status

from dtos import BlockResponseDTO, UpdateBlockDTO
from services.block_service import BlockService

from . import router

logger = logging.getLogger(__name__)


@router.patch("/{block_id}", response_model=BlockResponseDTO, status_code=status.HTTP_200_OK)
async def update_block(request: Request, block_id: str, data: UpdateBlockDTO) -> BlockResponseDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"User {user_id} updating block {block_id}")

        block = BlockService.update_block(client, block_id, data, locale)

        if not block:
            raise HTTPException(status_code=404, detail="Block not found")

        return block
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating block: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update block: {str(e)}")
