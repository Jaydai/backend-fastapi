from dataclasses import dataclass


@dataclass
class Message:
    id: str
    user_id: str
    message_provider_id: str
    content: str
    role: str
    chat_provider_id: str
    model: str
    created_at: str | None = None
    parent_message_provider_id: str | None = None


@dataclass
class Chat:
    id: str
    user_id: str
    chat_provider_id: str
    title: str
    provider_name: str
    created_at: str | None = None
