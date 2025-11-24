"""
Delete Template Version Route
Allows deletion of a specific template version
"""

import logging

from fastapi import HTTPException, Request, status

from . import router
from core.supabase import supabase
from services import PermissionService
from domains.enums import PermissionEnum

logger = logging.getLogger(__name__)


@router.delete("/{template_id}/versions/{version_id}", status_code=status.HTTP_200_OK)
async def delete_template_version(request: Request, template_id: str, version_id: str) -> dict:
    """
    Delete a specific version of a template

    **Authentication required**

    Args:
    - **template_id**: The ID of the template
    - **version_id**: The ID of the version to delete

    Returns:
    - Success message

    Raises:
    - 400: If trying to delete the current/default version
    - 403: If user doesn't have permission to delete this version
    - 404: If version not found
    - 500: If deletion fails
    """
    try:
        user_id = request.state.user_id
        supabase_client = request.state.supabase_client

        logger.info(f"User {user_id} attempting to delete version {version_id} of template {template_id}")

        # First, check if the version exists and get its details
        version_response = (
            supabase_client.table("prompt_templates_versions")
            .select("id, template_id, name, is_current")
            .eq("id", version_id)
            .eq("template_id", template_id)
            .single()
            .execute()
        )

        if not version_response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template version not found")

        version = version_response.data

        # Prevent deletion of the current/default version
        if version.get("is_current"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete the current version. Please set another version as current first.",
            )

        # Check if user has permission (template owner or organization admin)
        template_response = (
            supabase_client.table("prompt_templates")
            .select("user_id, organization_id")
            .eq("id", template_id)
            .single()
            .execute()
        )

        if not template_response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")

        template = template_response.data

        # Check if user is the template owner
        has_permission = template.get("user_id") == user_id

        # If template belongs to an organization, check organization permissions using new system
        if not has_permission and template.get("organization_id"):
            has_permission = PermissionService.user_has_permission_in_organization(
                supabase_client,
                user_id,
                PermissionEnum.TEMPLATE_DELETE,
                template["organization_id"]
            )

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this template version",
            )

        # Delete the version
        delete_response = (
            supabase_client.table("prompt_templates_versions")
            .delete()
            .eq("id", version_id)
            .eq("template_id", template_id)
            .execute()
        )

        logger.info(
            f"Successfully deleted version {version_id} (v{version['name']}) "
            f"of template {template_id} by user {user_id}"
        )

        return {
            "success": True,
            "message": f"Version {version['name']} deleted successfully",
            "deleted_version_id": version_id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete version {version_id} of template {template_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete template version: {str(e)}"
        )
