"""
Set Default Template Version Route
Sets a specific version as the current/default version
"""
from fastapi import HTTPException, Request, status
import logging

from . import router
from services import PermissionService
from domains.enums import PermissionEnum

logger = logging.getLogger(__name__)


@router.post(
    "/{template_id}/set-default",
    status_code=status.HTTP_200_OK
)
async def set_default_version(
    request: Request,
    template_id: str,
) -> dict:
    """
    Set a specific version as the current/default version

    **Authentication required**

    Args:
    - **template_id**: The ID of the template
    - **version_id**: The ID of the version to set as default (from request body)

    Returns:
    - Success message with updated data

    Raises:
    - 403: If user doesn't have permission
    - 404: If template or version not found
    - 500: If update fails
    """
    try:
        user_id = request.state.user_id
        supabase_client = request.state.supabase_client

        # Get JSON body
        body = await request.json()
        version_id = body.get("version_id")

        if not version_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="version_id is required in request body"
            )

        logger.info(
            f"User {user_id} attempting to set version {version_id} as default for template {template_id}"
        )

        # Check if version exists and belongs to this template
        version_response = (
            supabase_client.table("prompt_templates_versions")
            .select("id, template_id, name")
            .eq("id", version_id)
            .eq("template_id", template_id)
            .single()
            .execute()
        )

        if not version_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template version not found"
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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )

        template = template_response.data

        # Check if user is the template owner
        has_permission = template.get("user_id") == user_id

        # If template belongs to an organization, check organization permissions using new system
        if not has_permission and template.get("organization_id"):
            has_permission = PermissionService.user_has_permission_in_organization(
                supabase_client,
                user_id,
                PermissionEnum.TEMPLATE_UPDATE,
                template["organization_id"]
            )

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this template"
            )

        # Unset all other versions as current
        supabase_client.table("prompt_templates_versions").update({
            "is_current": False
        }).eq("template_id", template_id).execute()

        # Set this version as current
        version_update_response = (
            supabase_client.table("prompt_templates_versions")
            .update({"is_current": True})
            .eq("id", version_id)
            .eq("template_id", template_id)
            .execute()
        )

        # Update the template's current_version_id
        template_update_response = (
            supabase_client.table("prompt_templates")
            .update({"current_version_id": version_id})
            .eq("id", template_id)
            .execute()
        )

        logger.info(
            f"Successfully set version {version_id} as default for template {template_id} by user {user_id}"
        )

        return {
            "success": True,
            "message": f"Version {version_response.data['name']} set as default",
            "data": {
                "template_id": template_id,
                "current_version_id": version_id
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Failed to set default version for template {template_id}: {e}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set default version: {str(e)}"
        )
