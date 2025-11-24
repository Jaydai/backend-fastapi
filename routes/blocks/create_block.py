import logging

from fastapi import HTTPException, Request, status

from dtos import BlockResponseDTO, CreateBlockDTO
from services.block_service import BlockService

from . import router

logger = logging.getLogger(__name__)


@router.post("", response_model=BlockResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_block(request: Request, data: CreateBlockDTO) -> BlockResponseDTO:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"User {user_id} creating block: {data.title}")

        block = BlockService.create_block(client, user_id, data, locale)

        return block
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating block: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create block: {str(e)}")
