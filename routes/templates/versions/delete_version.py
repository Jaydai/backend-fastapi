"""
Delete Template Version Route
Allows deletion of a specific template version
"""

import logging

from fastapi import HTTPException, Request, status

from domains.enums import PermissionEnum
from routes.dependencies import require_permission_in_organization
from services import TemplateVersionService

from . import router

logger = logging.getLogger(__name__)


@router.delete("/{template_id}/versions/{version_id}", status_code=status.HTTP_200_OK)
@require_permission_in_organization(PermissionEnum.TEMPLATE_DELETE)
async def delete_template_version(request: Request, template_id: str, version_id: int) -> dict:
    """Delete a specific version of a template"""
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client

        logger.info(f"User {user_id} attempting to delete version {version_id} of template {template_id}")

        result = TemplateVersionService.delete_version(client, version_id, template_id)

        if result.get("error"):
            if result["error"] == "not_found":
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template version not found")
            elif result["error"] == "is_default":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot delete the current version. Please set another version as current first.",
                )
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["error"])

        logger.info(f"Successfully deleted version {version_id} of template {template_id} by user {user_id}")

        return {
            "success": True,
            "message": "Version deleted successfully",
            "deleted_version_id": version_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete version {version_id} of template {template_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete template version: {str(e)}"
        )
