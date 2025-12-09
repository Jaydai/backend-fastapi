"""
PATCH /onboarding/step

Updates the current onboarding step for the authenticated user.
"""

import logging

from fastapi import HTTPException, Request, status

from dtos.onboarding_dto import OnboardingFlowResponseDTO, UpdateOnboardingStepDTO
from services.onboarding_flow_service import OnboardingFlowService

from . import router

logger = logging.getLogger(__name__)


@router.patch("/step", response_model=OnboardingFlowResponseDTO, status_code=status.HTTP_200_OK)
async def update_onboarding_step(
    request: Request, data: UpdateOnboardingStepDTO
) -> OnboardingFlowResponseDTO:
    """
    Update the current onboarding step.

    Body:
    - step: The new step to set
    - flow_type: Optional flow type to set (if not already set)

    Returns the updated onboarding flow state.
    """
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} updating onboarding step to {data.step}")

        result = OnboardingFlowService.update_step(
            request.state.supabase_client, user_id, data
        )

        logger.info(f"User {user_id} onboarding step updated to {result.current_step}")
        return result

    except ValueError as e:
        logger.warning(f"Failed to update onboarding step: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating onboarding step: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update onboarding step: {str(e)}",
        )
