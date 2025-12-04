import logging

from fastapi import HTTPException, Request, status

from domains.enums import PermissionEnum
from dtos import BlockSummaryResponseDTO
from routes.dependencies import require_permission_in_organization
from services import BlockService

from . import router

logger = logging.getLogger(__name__)


@router.get("/{organization_id}/blocks", response_model=list[BlockSummaryResponseDTO])
@require_permission_in_organization(PermissionEnum.ORGANIZATION_READ)
async def get_organization_blocks(
    request: Request,
    organization_id: str,
    type: str | None = None,
) -> list[BlockSummaryResponseDTO]:
    locale = request.state.locale
    organization_id = request.state.organization_id
    try:
        # Fetch all blocks for the organization (minimal data for tree building)
        blocks = BlockService.get_blocks(
            request.state.supabase_client,
            locale=locale,
            user_id=None,
            organization_id=organization_id,
            type=type,
            limit=1000,
            offset=0,
        )
        return blocks

    except Exception as e:
        logger.error(f"Error fetching blocks for organization {organization_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch blocks: {str(e)}"
        )
