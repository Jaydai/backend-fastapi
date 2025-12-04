import logging

from fastapi import HTTPException, Request, status
from dtos import BlockSummaryResponseDTO
from services import BlockService

from . import router

logger = logging.getLogger(__name__)


@router.get("/blocks", response_model=list[BlockSummaryResponseDTO])
async def get_organization_blocks(
    request: Request,
    type: str | None = None,
) -> list[BlockSummaryResponseDTO]:
    locale = request.state.locale
    user_id = request.state.user_id
    try:
        # Fetch all blocks for the organization (minimal data for tree building)
        blocks = BlockService.get_blocks(
            request.state.supabase_client,
            locale=locale,
            user_id=user_id,
            organization_id=None,
            type=type,
            limit=1000,
            offset=0,
        )
        return blocks

    except Exception as e:
        logger.error(f"Error fetching blocks for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch blocks: {str(e)}"
        )
