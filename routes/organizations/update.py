"""
PUT /organizations/{organization_id} endpoint

Update organization details (name, description, image_url, website_url).
"""

import logging

from fastapi import HTTPException, Request, status
from pydantic import BaseModel

from repositories.organization_repository import OrganizationRepository

from . import router

logger = logging.getLogger(__name__)


class UpdateOrganizationRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    image_url: str | None = None
    website_url: str | None = None


@router.put("/{organization_id}")
async def update_organization(
    request: Request,
    organization_id: str,
    body: UpdateOrganizationRequest,
) -> dict:
    """
    Update an organization's details.

    Only admins can update organization details.
    """
    try:
        user_id = request.state.user_id
    except AttributeError:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    client = request.state.supabase_client

    # Check if user has admin role in this organization
    role_response = (
        client.table("user_organization_roles")
        .select("role")
        .eq("organization_id", organization_id)
        .eq("user_id", user_id)
        .execute()
    )

    if not role_response.data or len(role_response.data) == 0:
        raise HTTPException(status_code=403, detail="You are not a member of this organization")

    user_role = role_response.data[0]["role"]
    if user_role not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="Only admins can update organization details")

    # Update organization
    updated_org = OrganizationRepository.update_organization(
        client=client,
        organization_id=organization_id,
        name=body.name,
        description=body.description,
        image_url=body.image_url,
        website_url=body.website_url,
    )

    if not updated_org:
        raise HTTPException(status_code=404, detail="Organization not found")

    logger.info(f"[ORGANIZATIONS] Updated organization {organization_id} by user {user_id}")

    return {
        "id": updated_org.id,
        "name": updated_org.name,
        "type": updated_org.type,
        "image_url": updated_org.image_url,
        "banner_url": updated_org.banner_url,
        "website_url": updated_org.website_url,
        "created_at": updated_org.created_at,
    }
