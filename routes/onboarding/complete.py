"""
POST /onboarding/complete

Marks onboarding as complete for the authenticated user.
"""

import logging

from fastapi import HTTPException, Request, status

from dtos.onboarding_dto import OnboardingFlowResponseDTO
from services.onboarding_flow_service import OnboardingFlowService

from . import router

logger = logging.getLogger(__name__)


@router.post("/complete", response_model=OnboardingFlowResponseDTO, status_code=status.HTTP_200_OK)
async def complete_onboarding(request: Request) -> OnboardingFlowResponseDTO:
    """
    Mark onboarding as complete.

    This endpoint:
    1. Sets the onboarding step to 'completed'
    2. Records the completion timestamp
    3. Returns the final onboarding state
    """
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} completing onboarding")

        result = OnboardingFlowService.complete_onboarding(
            request.state.supabase_client, user_id
        )

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
