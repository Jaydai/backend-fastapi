from fastapi import HTTPException, Request, status
import logging

from . import router
from services import MessageService, ChatService
from dtos import CombinedBatchDTO, CombinedBatchResponseDTO

logger = logging.getLogger(__name__)


@router.post("/save-messages-and-chats", response_model=CombinedBatchResponseDTO, status_code=status.HTTP_201_CREATED)
async def save_messages_and_chats(
    request: Request,
    batch_data: CombinedBatchDTO
) -> CombinedBatchResponseDTO:
    try:
        user_id = request.state.user_id
        messages_count = len(batch_data.messages) if batch_data.messages else 0
        chats_count = len(batch_data.chats) if batch_data.chats else 0

        logger.info(
            f"User {user_id} saving combined batch: "
            f"{messages_count} messages, {chats_count} chats"
        )

        message_responses = []
        chat_responses = []
        message_stats = {"saved_count": 0, "skipped_count": 0, "total_count": 0}
        chat_stats = {"inserted_count": 0, "updated_count": 0, "total_count": 0}

        if batch_data.messages:
            message_responses, message_result = MessageService.save_messages_batch(
                request.state.supabase_client,
                user_id,
                batch_data.messages
            )
            message_stats = {
                "saved_count": message_result.saved_count,
                "skipped_count": message_result.skipped_count,
                "total_count": message_result.total_count
            }

        if batch_data.chats:
            chat_responses, chat_result = ChatService.save_chats_batch(
                request.state.supabase_client,
                user_id,
                batch_data.chats
            )
            chat_stats = {
                "inserted_count": chat_result.inserted_count,
                "updated_count": chat_result.updated_count,
                "total_count": chat_result.total_count
            }

        logger.info(
            f"Combined batch completed for user {user_id}: "
            f"messages={message_stats['saved_count']}/{message_stats['total_count']}, "
            f"chats={chat_stats['inserted_count']+chat_stats['updated_count']}/{chat_stats['total_count']}"
        )

        return CombinedBatchResponseDTO(
            messages=message_responses,
            chats=chat_responses,
            stats={
                "messages": message_stats,
                "chats": chat_stats
            }
        )

    except ValueError as e:
        logger.warning(f"Failed to save combined batch: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error saving combined batch: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save combined batch: {str(e)}"
        )
