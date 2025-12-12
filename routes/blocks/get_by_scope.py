"""
Route: GET /blocks/by-scope/{scope}
Get blocks filtered by scope (private, organization, or team)
"""
import logging

from fastapi import HTTPException, Query, Request, status

from dtos import BlockSummaryResponseDTO
from services.block_service import BlockService

from . import router

logger = logging.getLogger(__name__)


@router.get("/by-scope/{scope}", response_model=list[BlockSummaryResponseDTO], status_code=status.HTTP_200_OK)
async def get_blocks_by_scope(
    request: Request,
    scope: str,
    organization_id: str | None = Query(None, description="Organization ID (required for 'organization' scope)"),
    team_id: str | None = Query(None, description="Team ID (required for 'team' scope)"),
    type: str | None = Query(None, description="Filter by block type"),
    limit: int = Query(100, le=1000),
    offset: int = Query(0, ge=0),
) -> list[BlockSummaryResponseDTO]:
    """
    Get blocks filtered by scope.

    Scopes:
    - private: User's personal blocks
    - organization: Organization-wide blocks (requires organization_id)
    - team: Team-specific blocks (requires team_id)
    """
    try:
        client = request.state.supabase_client
        user_id = request.state.user_id
        locale = request.state.locale

        # Validate scope
        if scope not in ["private", "organization", "team"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid scope: {scope}. Must be one of: private, organization, team"
            )

        # Validate required parameters for each scope
        if scope == "organization" and not organization_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="organization_id is required for 'organization' scope"
            )

        if scope == "team" and not team_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="team_id is required for 'team' scope"
            )

        logger.info(f"Fetching blocks by scope={scope}, org={organization_id}, team={team_id}")

        blocks = BlockService.get_blocks_by_scope(
            client=client,
            user_id=user_id,
            scope=scope,
            locale=locale,
            organization_id=organization_id,
            team_id=team_id,
            type=type,
            limit=limit,
            offset=offset,
        )

        logger.info(f"Returning {len(blocks)} blocks for scope={scope}")
        return blocks

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching blocks by scope: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch blocks: {str(e)}"
        )
