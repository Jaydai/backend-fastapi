import logging
from fastapi import Body, HTTPException, Request, status
from domains.enums import PermissionEnum
from routes.dependencies import require_permission_in_organization
from dtos import UpdateTemplateVersionDTO
from services import TemplateVersionService
from repositories import TemplateRepository, TemplateVersionRepository

from . import router

logger = logging.getLogger(__name__)


@router.patch("/{template_id}/versions/{version_id}", status_code=status.HTTP_200_OK, response_model=UpdateTemplateVersionDTO)
@require_permission_in_organization(PermissionEnum.TEMPLATE_UPDATE)

async def update_version(
    request: Request,
    template_id: str,
    version_id: int,
    update_data: UpdateTemplateVersionDTO
) -> dict:
    print(f"💕💕💕💕💕💕💕💕💕💕💕💕 update_data: {update_data}")
    try:
        user_id = request.state.user_id
        supabase_client = request.state.supabase_client
        locale = request.state.locale

        version = TemplateVersionRepository.get_version_by_id(supabase_client, version_id)
        if not version:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template version not found")

        template = TemplateRepository.get_template_by_id(supabase_client, template_id)
        if not template:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")


        updated_version = TemplateVersionService.update_version(
            supabase_client, version_id, template_id, update_data, locale
        )
        if not updated_version:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update version")

        logger.info(f"Successfully updated version {version_id} of template {template_id} by user {user_id}")

        return updated_version 

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update version {version_id} of template {template_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update template version: {str(e)}"
        )
