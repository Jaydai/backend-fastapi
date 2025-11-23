"""
Update Template Version Route
Allows updating a specific template version's properties
"""
from fastapi import HTTPException, Request, status, Body
from pydantic import BaseModel
import logging

from . import router
from core.supabase import supabase
from services import PermissionService
from domains.enums import PermissionEnum

logger = logging.getLogger(__name__)


class UpdateVersionDTO(BaseModel):
    """DTO for updating version properties"""
    content: str | None = None
    change_notes: str | None = None
    status: str | None = None
    is_current: bool | None = None
    is_published: bool | None = None
    optimized_for: list[str] | None = None


@router.patch(
    "/{template_id}/versions/{version_id}",
    status_code=status.HTTP_200_OK
)
async def update_template_version(
    request: Request,
    template_id: str,
    version_id: int,
    update_data: UpdateVersionDTO = Body(...)
) -> dict:
    """
    Update a specific version of a template

    **Authentication required**

    Args:
    - **template_id**: The ID of the template
    - **version_id**: The ID of the version to update
    - **content**: New content (optional)
    - **change_notes**: New change notes (optional)
    - **status_val**: New status (optional)
    - **is_current**: Set as current version (optional)
    - **is_published**: Set publish status (optional)
    - **optimized_for**: List of AI tool IDs (optional)

    Returns:
    - Updated version data

    Raises:
    - 403: If user doesn't have permission
    - 404: If version not found
    - 500: If update fails
    """
    try:
        user_id = request.state.user_id
        supabase_client = request.state.supabase_client

        logger.info(
            f"User {user_id} attempting to update version {version_id} of template {template_id}"
        )

        # Check if version exists
        version_response = (
            supabase_client.table("prompt_templates_versions")
            .select("id, template_id")
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
                detail="You don't have permission to update this template version"
            )

        # Build update data from DTO, excluding None values
        update_dict = {}
        if update_data.content is not None:
            update_dict["content"] = update_data.content
        if update_data.change_notes is not None:
            update_dict["change_notes"] = update_data.change_notes
        if update_data.status is not None:
            update_dict["status"] = update_data.status
        if update_data.is_current is not None:
            update_dict["is_current"] = update_data.is_current
        if update_data.is_published is not None:
            update_dict["is_published"] = update_data.is_published
        if update_data.optimized_for is not None:
            update_dict["optimized_for"] = update_data.optimized_for

        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No update data provided"
            )

        # If setting as current, unset other versions first
        if update_dict.get("is_current") is True:
            supabase_client.table("prompt_templates_versions").update({
                "is_current": False
            }).eq("template_id", template_id).execute()

            # Also update the template's current_version_id
            supabase_client.table("prompt_templates").update({
                "current_version_id": version_id
            }).eq("id", template_id).execute()

        # Update the version
        update_response = (
            supabase_client.table("prompt_templates_versions")
            .update(update_dict)
            .eq("id", version_id)
            .eq("template_id", template_id)
            .execute()
        )

        if not update_response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update version"
            )

        logger.info(
            f"Successfully updated version {version_id} of template {template_id} by user {user_id}"
        )

        return {
            "success": True,
            "message": "Version updated successfully",
            "data": update_response.data[0] if update_response.data else None
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Failed to update version {version_id} of template {template_id}: {e}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update template version: {str(e)}"
        )
