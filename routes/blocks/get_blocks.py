from fastapi import Request, Query, HTTPException, status
import logging
from . import router
from services.block_service import BlockService
from dtos import BlockResponseDTO

logger = logging.getLogger(__name__)

@router.get("", response_model=list[BlockResponseDTO], status_code=status.HTTP_200_OK)
async def get_blocks(
    request: Request,
    block_type: str | None = Query(None, alias="type"),
    workspace_type: str | None = Query(None),
    organization_id: str | None = None,
    company_id: str | None = None,
    published: bool | None = None,
    q: str | None = None
) -> list[BlockResponseDTO]:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.headers.get("Accept-Language", "en").split(",")[0][:2]

        logger.info(f"User {user_id} getting blocks")

        blocks = BlockService.get_blocks(
            client,
            user_id,
            locale,
            block_type,
            workspace_type,
            organization_id,
            company_id,
            published,
            q
        )

        return blocks
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting blocks: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get blocks: {str(e)}")
