from fastapi import Request
from services.organization_service import OrganizationService
from dtos.organization_dto import InvitationResponseDTO
from routes.dependencies import require_permission_in_organization
from domains.enums import PermissionEnum
from . import router


@router.get("/{organization_id}/invitations", response_model=list[InvitationResponseDTO])
@require_permission_in_organization(PermissionEnum.ORGANIZATION_READ)
async def get_organization_invitations(
    request: Request,
    organization_id: str
) -> list[InvitationResponseDTO]:
    invitations = OrganizationService.get_organization_invitations(
        request.state.supabase_client,
        organization_id
    )
    return invitations
