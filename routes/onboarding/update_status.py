import logging

from fastapi import HTTPException, Request, status

from dtos.onboarding_dto import OnboardingStatusResponseDTO, UpdateOnboardingDTO
from services.onboarding_service import OnboardingService

from . import router

logger = logging.getLogger(__name__)


@router.patch("/status", response_model=OnboardingStatusResponseDTO, status_code=status.HTTP_200_OK)
async def update_onboarding_status(request: Request, update_data: UpdateOnboardingDTO) -> OnboardingStatusResponseDTO:
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} updating onboarding status")

        result = OnboardingService.update_onboarding(request.state.supabase_client, user_id, update_data)

        logger.info(f"User {user_id} onboarding status updated, completed: {result.has_completed_onboarding}")
        return result

    except ValueError as e:
        logger.warning(f"Failed to update onboarding status: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating onboarding status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update onboarding status: {str(e)}"
        )
