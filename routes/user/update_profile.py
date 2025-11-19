from fastapi import HTTPException, Request, status
import logging

from . import router
from services import UserService
from dtos import UserProfileResponseDTO, UpdateUserProfileDTO

logger = logging.getLogger(__name__)


@router.put(
    "/profile",
    response_model=UserProfileResponseDTO,
    status_code=status.HTTP_200_OK
)
async def update_user_profile(
    request: Request,
    update_data: UpdateUserProfileDTO
) -> UserProfileResponseDTO:
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} updating their profile")

        updated_profile = UserService.update_user_profile(
            request.state.supabase_client,
            user_id,
            update_data
        )

        logger.info(f"Successfully updated profile for user {user_id}")
        return updated_profile

    except ValueError as e:
        logger.warning(f"Failed to update user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user profile: {str(e)}"
        )
