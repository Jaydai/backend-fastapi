from fastapi import HTTPException, Request, status
import logging

from . import router
from services import MessageService
from dtos import SaveMessageDTO, MessageResponseDTO

logger = logging.getLogger(__name__)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_messages(
    request: Request,
    body: SaveMessageDTO | list[SaveMessageDTO]
) -> MessageResponseDTO | list[MessageResponseDTO]:
    try:
        user_id = request.state.user_id

        if isinstance(body, list):
            logger.info(f"User {user_id} creating batch of {len(body)} messages")

            messages_list, batch_result = MessageService.save_messages_batch(
                request.state.supabase_client,
                user_id,
                body
            )

            logger.info(
                f"Batch creation completed: {batch_result.saved_count} saved, "
                f"{batch_result.skipped_count} skipped"
            )
            return messages_list
        else:
            logger.info(f"User {user_id} creating message {body.message_provider_id}")

            result = MessageService.save_message(
                request.state.supabase_client,
                user_id,
                body
            )

            logger.info(f"Message {body.message_provider_id} created successfully")
            return result

    except ValueError as e:
        logger.warning(f"Failed to create messages: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating messages: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create messages: {str(e)}"
        )
