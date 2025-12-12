"""
PATCH /onboarding/status

Updates the legacy onboarding status for the authenticated user.
This endpoint is for backward compatibility with older clients.
"""

import logging

from fastapi import HTTPException, status

from dtos.onboarding_dto import OnboardingStatusResponseDTO, UpdateOnboardingDTO
from services.onboarding_service import OnboardingService
from utils.dependencies import AuthenticatedUser, SupabaseClient

from . import router

logger = logging.getLogger(__name__)


@router.patch(
    "/status",
    response_model=OnboardingStatusResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def update_onboarding_status(
    user_id: AuthenticatedUser,
    client: SupabaseClient,
    update_data: UpdateOnboardingDTO,
) -> OnboardingStatusResponseDTO:
    """
    Update legacy onboarding status.

    This endpoint updates the users_metadata table for backward compatibility.
    For new implementations, use the /flow and /step endpoints instead.
    """
    try:
        logger.info(f"User {user_id} updating onboarding status")

        result = OnboardingService.update_onboarding(client, user_id, update_data)

        logger.info(
            f"User {user_id} onboarding status updated, completed: {result.has_completed_onboarding}"
        )
        return result

    except ValueError as e:
        logger.warning(f"Failed to update onboarding status: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating onboarding status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update onboarding status: {str(e)}",
        )
