from fastapi import HTTPException, Request, status
import logging

from . import router
from services import ChatService
from dtos import SaveChatDTO, ChatResponseDTO

logger = logging.getLogger(__name__)


@router.post("", status_code=status.HTTP_200_OK)
async def create_chats(
    request: Request,
    body: SaveChatDTO | list[SaveChatDTO]
) -> ChatResponseDTO | list[ChatResponseDTO]:
    try:
        user_id = request.state.user_id

        if isinstance(body, list):
            logger.info(f"User {user_id} creating/updating batch of {len(body)} chats")

            chats_list, batch_result = ChatService.save_chats_batch(
                request.state.supabase_client,
                user_id,
                body
            )

            logger.info(
                f"Batch operation completed: {batch_result.inserted_count} inserted, "
                f"{batch_result.updated_count} updated"
            )
            return chats_list
        else:
            logger.info(f"User {user_id} creating/updating chat {body.chat_provider_id}")

            result = ChatService.save_chat(
                request.state.supabase_client,
                user_id,
                body
            )

            logger.info(f"Chat {body.chat_provider_id} created/updated successfully")
            return result

    except ValueError as e:
        logger.warning(f"Failed to create/update chats: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating/updating chats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create/update chats: {str(e)}"
        )
