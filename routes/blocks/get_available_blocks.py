import logging

from fastapi import HTTPException, Request, status

from dtos import BlockSummaryResponseDTO
from services import BlockService

from . import router

logger = logging.getLogger(__name__)


@router.get("", response_model=list[BlockSummaryResponseDTO])
async def get_available_blocks(
    request: Request,
    type: str | None = None,
) -> list[BlockSummaryResponseDTO]:
    locale = request.state.locale
    try:
        # Fetch all blocks for the organization (minimal data for tree building)
        blocks = BlockService.get_blocks(
            request.state.supabase_client,
            locale=locale,
            user_id=None,
            organization_id=None,
            type=type,
            include_org_info=True,
            limit=1000,
            offset=0,
        )
        return blocks

    except Exception as e:
        logger.error(f"Error fetching available blocks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch blocks: {str(e)}"
        )
