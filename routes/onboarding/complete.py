"""
POST /onboarding/complete

Marks onboarding as complete for the authenticated user.
"""

import logging

from fastapi import HTTPException, status

from dtos.onboarding_dto import OnboardingFlowResponseDTO
from services.onboarding_flow_service import OnboardingFlowService
from utils.dependencies import AuthenticatedUser, SupabaseClient

from . import router

logger = logging.getLogger(__name__)


@router.post(
    "/complete",
    response_model=OnboardingFlowResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def complete_onboarding(
    user_id: AuthenticatedUser,
    client: SupabaseClient,
) -> OnboardingFlowResponseDTO:
    """
    Mark onboarding as complete.

    This endpoint:
    1. Sets the onboarding step to 'completed'
    2. Records the completion timestamp
    3. Returns the final onboarding state
    """
    try:
        logger.info(f"User {user_id} completing onboarding")

        result = OnboardingFlowService.complete_onboarding(client, user_id)

        logger.info(f"User {user_id} completed onboarding")
        return result

    except ValueError as e:
        logger.warning(f"Failed to complete onboarding: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error completing onboarding: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete onboarding: {str(e)}",
        )
