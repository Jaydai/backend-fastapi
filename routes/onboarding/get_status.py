"""
GET /onboarding/status

Returns the legacy onboarding status for the authenticated user.
This endpoint is for backward compatibility with older clients.
"""

import logging

from fastapi import HTTPException, status

from dtos.onboarding_dto import OnboardingStatusResponseDTO
from services.onboarding_service import OnboardingService
from utils.dependencies import AuthenticatedUser, SupabaseClient

from . import router

logger = logging.getLogger(__name__)


@router.get(
    "/status",
    response_model=OnboardingStatusResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def get_onboarding_status(
    user_id: AuthenticatedUser,
    client: SupabaseClient,
) -> OnboardingStatusResponseDTO:
    """
    Get legacy onboarding status.

    This endpoint reads from the users_metadata table for backward compatibility.
    For new implementations, use the /flow endpoint instead.
    """
    try:
        logger.info(f"User {user_id} getting onboarding status")

        result = OnboardingService.get_onboarding_status(client, user_id)

        logger.info(
            f"User {user_id} onboarding status retrieved, completed: {result.has_completed_onboarding}"
        )
        return result

    except ValueError as e:
        logger.warning(f"Failed to get onboarding status: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting onboarding status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get onboarding status: {str(e)}",
        )
