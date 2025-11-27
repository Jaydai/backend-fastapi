from fastapi import Request, HTTPException, status
import logging
from . import router
from services.block_service import BlockService
from dtos import BlockResponseDTO

logger = logging.getLogger(__name__)

@router.get("/{block_id}", response_model=BlockResponseDTO, status_code=status.HTTP_200_OK)
async def get_block(
    request: Request,
    block_id: str
) -> BlockResponseDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"User {user_id} getting block {block_id}")

        block = BlockService.get_block_by_id(client, block_id, locale)

        if not block:
            raise HTTPException(status_code=404, detail="Block not found")

        return block
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting block: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get block: {str(e)}")
