from fastapi import HTTPException, Request, status
import logging

from . import router
from services import UserService
from dtos import UserProfileResponseDTO

logger = logging.getLogger(__name__)


@router.get(
    "/profile",
    response_model=UserProfileResponseDTO,
    status_code=status.HTTP_200_OK
)
async def get_user_profile(request: Request) -> UserProfileResponseDTO:
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} fetching their profile")

        profile = UserService.get_user_profile(
            request.state.supabase_client,
            user_id
        )

        logger.info(f"Successfully retrieved profile for user {user_id}")
        return profile

    except ValueError as e:
        logger.warning(f"Failed to retrieve user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error retrieving user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user profile: {str(e)}"
        )
