"""
GET /user/templates/root
Returns folders and templates at root level or within a specific folder
RESTful endpoint for "mes templates" section in extension
"""
from fastapi import HTTPException, Request, Query, status
import logging
from typing import Optional

from . import router
from services import TemplateService, FolderService
from dtos import WorkspaceRootResponseDTO


logger = logging.getLogger(__name__)


@router.get(
    "/templates/root",
    response_model=WorkspaceRootResponseDTO
)
async def get_user_templates_root(
    request: Request,
    locale: str = Query("en", description="Locale for localization"),
    limit: int = Query(100, description="Maximum number of items per type", ge=1, le=1000),
    offset: int = Query(0, description="Offset for pagination", ge=0),
    folder_id: str | None = Query(None, description="Folder ID to get content from (omit or 'ROOT' for root level)")
) -> WorkspaceRootResponseDTO:
    """
    Get folders and templates at root level or within a specific folder for current user.

    **Query parameters:**
    - **folder_id**: UUID of parent folder, omit or "ROOT" for root level (default: None/ROOT)
    - **locale**: Language code (en, fr, etc.)
    - **limit**: Max items to return per type (default: 100)
    - **offset**: Pagination offset (default: 0)

    **Returns:**
    - folders: List of child folders
    - templates: List of templates in this folder/root
    - total_folders: Count of child folders
    - total_templates: Count of templates

    **Examples:**
    - GET /user/templates/root → Root level content
    - GET /user/templates/root?folder_id=ROOT → Root level content (explicit)
    - GET /user/templates/root?folder_id=123e4567-... → Content of specific folder
    """
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        # DEBUG: Log incoming parameters
        logger.info(f"[TEMPLATES_ROOT] Incoming params: folder_id={folder_id}, locale={locale}, limit={limit}, offset={offset}")

        # Normalize folder_id: None or "ROOT" means root level
        parent_folder_id = "ROOT" if (folder_id is None or folder_id == "ROOT") else folder_id
        template_folder_id = "ROOT" if (folder_id is None or folder_id == "ROOT") else folder_id

        logger.info(f"[TEMPLATES_ROOT] Normalized: parent_folder_id={parent_folder_id}, template_folder_id={template_folder_id}")

        # Get child folders (parent_folder_id = specified folder or NULL for root)
        folders = FolderService.get_folders_titles(
            client=client,
            locale=locale,
            user_id=user_id,
            organization_id=None,
            parent_folder_id=parent_folder_id,
            limit=limit,
            offset=offset
        )

        # Get templates in this folder (folder_id = specified folder or NULL for root)
        templates = TemplateService.get_templates_titles(
            client=client,
            locale=locale,
            user_id=user_id,
            organization_id=None,
            folder_id=template_folder_id,
            published_only=None,
            limit=limit,
            offset=offset
        )

        return WorkspaceRootResponseDTO(
            folders=folders,
            templates=templates,
            total_folders=len(folders),
            total_templates=len(templates)
        )

    except Exception as e:
        logger.error(f"Error fetching user workspace content: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch workspace content: {str(e)}"
        )
