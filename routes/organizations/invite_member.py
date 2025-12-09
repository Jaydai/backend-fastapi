"""
POST /organizations/{organization_id}/invitations

Bulk invite members to an organization.
"""

import logging

from fastapi import HTTPException, Request, status

from dtos.organization_dto import BulkInviteDTO, BulkInviteResponseDTO
from services.organization_service import OrganizationService

from . import router

logger = logging.getLogger(__name__)


@router.post(
    "/{organization_id}/invitations",
    response_model=BulkInviteResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def invite_members(
    request: Request, organization_id: str, data: BulkInviteDTO
) -> BulkInviteResponseDTO:
    """
    Bulk invite members to an organization.

    Body:
    - emails: List of email addresses to invite (1-50)
    - role: Role to assign ('admin', 'writer', 'viewer', 'guest'), default 'viewer'

    Returns:
    - successful: List of successfully invited emails
    - failed: List of failed emails with reasons
    - total_invited: Count of successful invitations
    """
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} inviting {len(data.emails)} members to org {organization_id}")

        result = OrganizationService.bulk_invite_members(
            client=request.state.supabase_client,
            organization_id=organization_id,
            inviter_id=user_id,
            emails=data.emails,
            role=data.role,
        )

        logger.info(
            f"Bulk invite to org {organization_id}: {result.total_invited} successful, {len(result.failed)} failed"
        )
        return result

    except ValueError as e:
        logger.warning(f"Failed to invite members: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error inviting members: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to invite members: {str(e)}",
        )
