import logging

from dtos import TemplateTitleResponseDTO
from services.template_service import TemplateService

from . import router

logger = logging.getLogger(__name__)


@router.get("", response_model=list[TemplateTitleResponseDTO], status_code=status.HTTP_200_OK)
async def get_all_templates(
    request: Request,
    organization_id: str | None = None,
    folder_ids: str | None = Query(
        None, description="Comma-separated folder IDs to filter templates. Empty for root only."
    ),
    published: bool | None = None,
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
) -> list[TemplateTitleResponseDTO]:
    """
    Get template titles (id, title) with optional filtering.
    Returns minimal data for list endpoints.

    Filters:
    - folder_ids: comma-separated IDs, empty string for root only, omit for all
    - published: filter by published status
    """
    try:
        client = request.state.supabase_client
        user_id = request.state.user_id
        locale = request.state.locale

        logger.info(
            f"Fetching template titles with folder_ids={folder_ids}, published={published}, organization_id={organization_id}"
        )

        # Parse folder_ids
        folder_id_list: list[str] | None = None
        if folder_ids is not None:
            if folder_ids == "":
                folder_id_list = []
            else:
                folder_id_list = [fid.strip() for fid in folder_ids.split(",") if fid.strip()]

        templates = TemplateService.get_templates_titles(
            client,
            locale,
            user_id,  # Pass user_id for personal templates
            organization_id,  # Pass organization_id for org templates
            folder_id_list,
            published,
            limit,
            offset,
        )

        logger.info(f"Returning {len(templates)} template titles")
        return templates

    except Exception as e:
        logger.error(f"Error fetching template titles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch template titles: {str(e)}"
        )
