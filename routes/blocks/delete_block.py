from fastapi import Request, HTTPException, status
import logging
from . import router
from services.block_service import BlockService

logger = logging.getLogger(__name__)

@router.delete("/{block_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_block(
    request: Request,
    block_id: str
):
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} deleting block {block_id}")

        success = BlockService.delete_block(client, block_id)

        if not success:
            raise HTTPException(status_code=404, detail="Block not found")

        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting block: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete block: {str(e)}")
