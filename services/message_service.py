import logging
from datetime import UTC, datetime

from supabase import Client

from dtos import (
    ChatBatchResultDTO,
    ChatResponseDTO,
    MessageBatchResultDTO,
    MessageResponseDTO,
    SaveChatDTO,
    SaveMessageDTO,
)
from repositories import ChatRepository, MessageRepository

logger = logging.getLogger(__name__)


class MessageService:
    @staticmethod
    def save_message(client: Client, user_id: str, message_dto: SaveMessageDTO) -> MessageResponseDTO:
        created_at = MessageService._convert_timestamp(message_dto.created_at)

        message_data = {
            "user_id": user_id,
            "message_provider_id": message_dto.message_provider_id,
            "content": message_dto.content,
            "role": message_dto.role,
            "chat_provider_id": message_dto.chat_provider_id,
            "model": message_dto.model,
            "created_at": created_at,
        }

        if message_dto.parent_message_provider_id:
            message_data["parent_message_provider_id"] = message_dto.parent_message_provider_id

        message = MessageRepository.save_message(client, message_data)

        if not message:
            raise ValueError("Failed to save message")

        return MessageResponseDTO(
            id=message.id,
            user_id=message.user_id,
            message_provider_id=message.message_provider_id,
            content=message.content,
            role=message.role,
            chat_provider_id=message.chat_provider_id,
            model=message.model,
            created_at=message.created_at,
            parent_message_provider_id=message.parent_message_provider_id,
        )

    @staticmethod
    def save_messages_batch(
        client: Client, user_id: str, messages: list[SaveMessageDTO]
    ) -> tuple[list[MessageResponseDTO], MessageBatchResultDTO]:
        if not messages:
            return [], MessageBatchResultDTO(saved_count=0, skipped_count=0, total_count=0)

        messages_to_upsert = []
        for message in messages:
            created_at = MessageService._convert_timestamp(message.created_at)

            message_data = {
                "user_id": user_id,
                "message_provider_id": message.message_provider_id,
                "content": message.content,
                "role": message.role,
                "chat_provider_id": message.chat_provider_id,
                "model": message.model,
                "created_at": created_at,
            }

            if message.parent_message_provider_id:
                message_data["parent_message_provider_id"] = message.parent_message_provider_id

            messages_to_upsert.append(message_data)

        upserted_messages = MessageRepository.upsert_messages_batch(client, messages_to_upsert)

        response_dtos = [
            MessageResponseDTO(
                id=msg.id,
                user_id=msg.user_id,
                message_provider_id=msg.message_provider_id,
                content=msg.content,
                role=msg.role,
                chat_provider_id=msg.chat_provider_id,
                model=msg.model,
                created_at=msg.created_at,
                parent_message_provider_id=msg.parent_message_provider_id,
            )
            for msg in upserted_messages
        ]

        result_dto = MessageBatchResultDTO(
            saved_count=len(upserted_messages), skipped_count=0, total_count=len(messages)
        )

        return response_dtos, result_dto

    @staticmethod
    def _convert_timestamp(timestamp: float | None) -> str:
        if timestamp:
            try:
                timestamp_in_seconds = timestamp / 1000 if timestamp > 1e10 else timestamp
                return datetime.fromtimestamp(timestamp_in_seconds, tz=UTC).isoformat()
            except Exception:
                return datetime.now(tz=UTC).isoformat()
        return datetime.now(tz=UTC).isoformat()


class ChatService:
    @staticmethod
    def save_chat(client: Client, user_id: str, chat_dto: SaveChatDTO) -> ChatResponseDTO:
        existing_chat = ChatRepository.get_chat_by_provider_id(client, user_id, chat_dto.chat_provider_id)

        if existing_chat:
            update_data = {"title": chat_dto.title, "provider_name": chat_dto.provider_name}
            updated_chat = ChatRepository.update_chat(client, user_id, chat_dto.chat_provider_id, update_data)
            chat = updated_chat if updated_chat else existing_chat
        else:
            chat_data = {
                "user_id": user_id,
                "chat_provider_id": chat_dto.chat_provider_id,
                "title": chat_dto.title,
                "provider_name": chat_dto.provider_name,
            }
            chat = ChatRepository.create_chat(client, chat_data)

        if not chat:
            raise ValueError("Failed to save chat")

        return ChatResponseDTO(
            id=chat.id,
            user_id=chat.user_id,
            chat_provider_id=chat.chat_provider_id,
            title=chat.title,
            provider_name=chat.provider_name,
            created_at=chat.created_at,
        )

    @staticmethod
    def save_chats_batch(
        client: Client, user_id: str, chats: list[SaveChatDTO]
    ) -> tuple[list[ChatResponseDTO], ChatBatchResultDTO]:
        if not chats:
            return [], ChatBatchResultDTO(inserted_count=0, updated_count=0, total_count=0)

        chat_ids = [chat.chat_provider_id for chat in chats]
        existing_ids = ChatRepository.get_existing_chat_ids(client, user_id, chat_ids)

        chats_to_insert = []
        updated_count = 0

        for chat in chats:
            if chat.chat_provider_id in existing_ids:
                update_data = {"title": chat.title, "provider_name": chat.provider_name}
                ChatRepository.update_chat(client, user_id, chat.chat_provider_id, update_data)
                updated_count += 1
            else:
                chats_to_insert.append(
                    {
                        "user_id": user_id,
                        "chat_provider_id": chat.chat_provider_id,
                        "title": chat.title,
                        "provider_name": chat.provider_name,
                    }
                )

        inserted_chats = ChatRepository.create_chats_batch(client, chats_to_insert)

        response_dtos = [
            ChatResponseDTO(
                id=chat.id,
                user_id=chat.user_id,
                chat_provider_id=chat.chat_provider_id,
                title=chat.title,
                provider_name=chat.provider_name,
                created_at=chat.created_at,
            )
            for chat in inserted_chats
        ]

        result_dto = ChatBatchResultDTO(
            inserted_count=len(inserted_chats), updated_count=updated_count, total_count=len(chats)
        )

        return response_dtos, result_dto
