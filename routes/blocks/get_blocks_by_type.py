import logging

from fastapi import HTTPException, Request, status

from dtos import BlockResponseDTO
from services.block_service import BlockService

from . import router

logger = logging.getLogger(__name__)


@router.get("/type/{block_type}", response_model=list[BlockResponseDTO], status_code=status.HTTP_200_OK)
async def get_blocks_by_type(request: Request, block_type: str) -> list[BlockResponseDTO]:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"User {user_id} getting blocks by type {block_type}")

        blocks = BlockService.get_blocks(client, user_id, locale, block_type=block_type)

        return blocks
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting blocks by type: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get blocks by type: {str(e)}")
