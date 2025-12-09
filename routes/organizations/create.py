"""
POST /organizations

Creates a new organization and sets the creator as admin.
"""

import logging

from fastapi import HTTPException, Request, status

from dtos.organization_dto import CreateOrganizationDTO, OrganizationDetailResponseDTO
from services.organization_service import OrganizationService

from . import router

logger = logging.getLogger(__name__)


@router.post("", response_model=OrganizationDetailResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_organization(request: Request, data: CreateOrganizationDTO) -> OrganizationDetailResponseDTO:
    logger.info(f"Creating organization: {data}")
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} creating organization: {data.name}")

        result = OrganizationService.create_organization(
            request.state.supabase_client, user_id, data
        )

        logger.info(f"Organization {result.id} created successfully by user {user_id}")
        return result

    except ValueError as e:
        logger.warning(f"Failed to create organization: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating organization: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create organization: {str(e)}",
        )
