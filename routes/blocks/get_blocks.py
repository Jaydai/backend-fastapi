import logging
from . import router
from services.block_service import BlockService
from dtos import BlockTitleResponseDTO

logger = logging.getLogger(__name__)

@router.get("", response_model=list[BlockTitleResponseDTO], status_code=status.HTTP_200_OK)
async def get_blocks(
    request: Request,
    organization_id: str | None = None,
    types: str | None = Query(None, description="Comma-separated block types to filter"),
    published: bool | None = None,
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0)
) -> list[BlockTitleResponseDTO]:
    """
    Get block titles (id, title) with optional filtering.
    Returns minimal data for list endpoints.

    Filters:
    - types: comma-separated block types
    - published: filter by published status
    """
    try:
        client = request.state.supabase_client
        locale = request.state.locale

        logger.info(f"Fetching block titles with types={types}, published={published}")

        # Parse types
        type_list: list[str] | None = None
        if types is not None:
            type_list = [t.strip() for t in types.split(",") if t.strip()]

        blocks = BlockService.get_blocks_titles(
            client,
            locale,
            organization_id,
            type_list,
            published,
            limit,
            offset
        )

        logger.info(f"Returning {len(blocks)} block titles")
        return blocks
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting block titles: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get block titles: {str(e)}")
