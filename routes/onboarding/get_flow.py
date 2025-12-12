"""
GET /onboarding/flow

Returns the current onboarding flow state for the authenticated user.
"""

import logging

from fastapi import HTTPException, status

from dtos.onboarding_dto import OnboardingFlowResponseDTO
from services.onboarding_flow_service import OnboardingFlowService
from utils.dependencies import AuthenticatedUser, SupabaseClient

from . import router

logger = logging.getLogger(__name__)


@router.get(
    "/flow",
    response_model=OnboardingFlowResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def get_onboarding_flow(
    user_id: AuthenticatedUser,
    client: SupabaseClient,
) -> OnboardingFlowResponseDTO:
    """
    Get the current onboarding flow state.

    Returns:
    - flow_type: 'invited', 'create_org', 'personal', or null
    - current_step: Current step in the onboarding flow
    - pending_invitation: Pending organization invitation if any
    - organization_id: User's organization if they have one
    - has_extension: Whether the Chrome extension is installed
    - has_completed_onboarding: Whether onboarding is complete
    """
    try:
        logger.info(f"User {user_id} getting onboarding flow")

        result = OnboardingFlowService.get_onboarding_flow(client, user_id)

        logger.info(
            f"User {user_id} onboarding flow: type={result.flow_type}, step={result.current_step}"
        )
        return result

    except ValueError as e:
        logger.warning(f"Failed to get onboarding flow: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting onboarding flow: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get onboarding flow: {str(e)}",
        )
