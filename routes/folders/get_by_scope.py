import logging

from fastapi import HTTPException, Query, Request, status

from dtos import FolderTitleResponseDTO
from services.folder_service import FolderService

from . import router

logger = logging.getLogger(__name__)


@router.get("/by-scope/{scope}", response_model=list[FolderTitleResponseDTO], status_code=status.HTTP_200_OK)
async def get_folders_by_scope(
    request: Request,
    scope: str,  # 'private' | 'organization' | 'team'
    organization_id: str | None = Query(None),
    team_id: str | None = Query(None),
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
) -> list[FolderTitleResponseDTO]:
    """Get folders filtered by content scope.

    Args:
        scope: Content scope - 'private', 'organization', or 'team'
        organization_id: Required for 'organization' and 'team' scopes
        team_id: Required for 'team' scope
    """
    try:
        client = request.state.supabase_client
        locale = request.state.locale
        user_id = request.state.user_id

        # Validate scope
        if scope not in ("private", "organization", "team"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid scope: {scope}. Must be 'private', 'organization', or 'team'"
            )

        # Validate required params based on scope
        if scope == "organization" and not organization_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="organization_id is required for organization scope"
            )

        if scope == "team" and not team_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="team_id is required for team scope"
            )

        logger.info(
            f"User {user_id} fetching folders by scope={scope}, org={organization_id}, team={team_id}"
        )

        folders = FolderService.get_folders_by_scope(
            client,
            user_id,
            scope,
            locale,
            organization_id,
            team_id,
            limit,
            offset,
        )

        logger.info(f"Returning {len(folders)} folders for scope {scope}")
        return folders
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting folders by scope: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get folders: {str(e)}")
