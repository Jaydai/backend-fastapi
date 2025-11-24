import logging

from fastapi import HTTPException, Request, Response, status

from dtos import UpdateDataCollectionDTO
from services import UserService

from . import router

logger = logging.getLogger(__name__)


@router.put("/data-collection", status_code=status.HTTP_204_NO_CONTENT)
async def update_data_collection(request: Request, update_data: UpdateDataCollectionDTO) -> Response:
    try:
        user_id = request.state.user_id
        logger.info(f"User {user_id} updating data collection preference to {update_data.data_collection}")

        UserService.update_data_collection(request.state.supabase_client, user_id, update_data.data_collection)

        logger.info(f"Successfully updated data collection for user {user_id}")

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        logger.warning(f"Failed to update data collection: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating data collection: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update data collection: {str(e)}"
        )
