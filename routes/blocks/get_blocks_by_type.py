from fastapi import Request, HTTPException, status
import logging
from . import router
from services.block_service import BlockService
from dtos import BlockResponseDTO

logger = logging.getLogger(__name__)

@router.get("/type/{block_type}", response_model=list[BlockResponseDTO], status_code=status.HTTP_200_OK)
async def get_blocks_by_type(
    request: Request,
    block_type: str
) -> list[BlockResponseDTO]:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.headers.get("Accept-Language", "en").split(",")[0][:2]

        logger.info(f"User {user_id} getting blocks by type {block_type}")

        blocks = BlockService.get_blocks(
            client,
            user_id,
            locale,
            block_type=block_type
        )

        return blocks
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting blocks by type: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get blocks by type: {str(e)}")
