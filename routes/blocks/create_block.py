from fastapi import Request, HTTPException, status
import logging
from . import router
from services.block_service import BlockService
from dtos import CreateBlockDTO, BlockResponseDTO

logger = logging.getLogger(__name__)

@router.post("", response_model=BlockResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_block(
    request: Request,
    data: CreateBlockDTO
) -> BlockResponseDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.headers.get("Accept-Language", "en").split(",")[0][:2]

        logger.info(f"User {user_id} creating block: {data.title}")

        block = BlockService.create_block(client, user_id, data, locale)

        return block
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating block: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create block: {str(e)}")
