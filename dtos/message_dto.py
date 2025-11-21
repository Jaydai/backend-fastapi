from pydantic import BaseModel


class SaveMessageDTO(BaseModel):
    message_provider_id: str
    content: str
    role: str
    chat_provider_id: str
    model: str = "unknown"
    created_at: float | None = None
    parent_message_provider_id: str | None = None


class MessageResponseDTO(BaseModel):
    id: int
    user_id: str
    message_provider_id: str
    content: str
    role: str
    chat_provider_id: str
    model: str
    created_at: str | None = None
    parent_message_provider_id: str | None = None


class SaveChatDTO(BaseModel):
    chat_provider_id: str
    title: str
    provider_name: str = "ChatGPT"


class ChatResponseDTO(BaseModel):
    id: int
    user_id: str
    chat_provider_id: str
    title: str
    provider_name: str
    created_at: str | None = None


class MessageBatchResultDTO(BaseModel):
    saved_count: int
    skipped_count: int
    total_count: int


class ChatBatchResultDTO(BaseModel):
    inserted_count: int
    updated_count: int
    total_count: int


class CombinedBatchDTO(BaseModel):
    messages: list[SaveMessageDTO] | None = None
    chats: list[SaveChatDTO] | None = None


class CombinedBatchResponseDTO(BaseModel):
    messages: list[MessageResponseDTO]
    chats: list[ChatResponseDTO]
    stats: dict
