from domains.entities import Chat, Message
from supabase import Client


class MessageRepository:
    @staticmethod
    def save_message(client: Client, message_data: dict) -> Message | None:
        response = client.table("messages").insert(message_data).execute()

        if not response.data:
            return None

        row = response.data[0]
        return Message(
            id=row["id"],
            user_id=row["user_id"],
            message_provider_id=row["message_provider_id"],
            content=row["content"],
            role=row["role"],
            chat_provider_id=row["chat_provider_id"],
            model=row["model"],
            created_at=row.get("created_at"),
            parent_message_provider_id=row.get("parent_message_provider_id"),
        )

    @staticmethod
    def get_existing_message_ids(client: Client, user_id: str, message_ids: list[str]) -> set[str]:
        if not message_ids:
            return set()

        response = (
            client.table("messages")
            .select("message_provider_id")
            .eq("user_id", user_id)
            .in_("message_provider_id", message_ids)
            .execute()
        )

        if not response.data:
            return set()

        return {row["message_provider_id"] for row in response.data}

    @staticmethod
    def save_messages_batch(client: Client, messages_data: list[dict]) -> list[Message]:
        if not messages_data:
            return []

        response = client.table("messages").insert(messages_data).execute()

        if not response.data:
            return []

        return [
            Message(
                id=row["id"],
                user_id=row["user_id"],
                message_provider_id=row["message_provider_id"],
                content=row["content"],
                role=row["role"],
                chat_provider_id=row["chat_provider_id"],
                model=row["model"],
                created_at=row.get("created_at"),
                parent_message_provider_id=row.get("parent_message_provider_id"),
            )
            for row in response.data
        ]


class ChatRepository:
    @staticmethod
    def get_chat_by_provider_id(client: Client, user_id: str, chat_provider_id: str) -> Chat | None:
        response = (
            client.table("chats").select("*").eq("user_id", user_id).eq("chat_provider_id", chat_provider_id).execute()
        )

        if not response.data:
            return None

        row = response.data[0]
        return Chat(
            id=row["id"],
            user_id=row["user_id"],
            chat_provider_id=row["chat_provider_id"],
            title=row["title"],
            provider_name=row["provider_name"],
            created_at=row.get("created_at"),
        )

    @staticmethod
    def create_chat(client: Client, chat_data: dict) -> Chat | None:
        response = client.table("chats").insert(chat_data).execute()

        if not response.data:
            return None

        row = response.data[0]
        return Chat(
            id=row["id"],
            user_id=row["user_id"],
            chat_provider_id=row["chat_provider_id"],
            title=row["title"],
            provider_name=row["provider_name"],
            created_at=row.get("created_at"),
        )

    @staticmethod
    def update_chat(client: Client, user_id: str, chat_provider_id: str, update_data: dict) -> Chat | None:
        response = (
            client.table("chats")
            .update(update_data)
            .eq("user_id", user_id)
            .eq("chat_provider_id", chat_provider_id)
            .execute()
        )

        if not response.data:
            return None

        row = response.data[0]
        return Chat(
            id=row["id"],
            user_id=row["user_id"],
            chat_provider_id=row["chat_provider_id"],
            title=row["title"],
            provider_name=row["provider_name"],
            created_at=row.get("created_at"),
        )

    @staticmethod
    def get_existing_chat_ids(client: Client, user_id: str, chat_ids: list[str]) -> set[str]:
        if not chat_ids:
            return set()

        response = (
            client.table("chats")
            .select("chat_provider_id")
            .eq("user_id", user_id)
            .in_("chat_provider_id", chat_ids)
            .execute()
        )

        if not response.data:
            return set()

        return {row["chat_provider_id"] for row in response.data}

    @staticmethod
    def create_chats_batch(client: Client, chats_data: list[dict]) -> list[Chat]:
        if not chats_data:
            return []

        response = client.table("chats").insert(chats_data).execute()

        if not response.data:
            return []

        return [
            Chat(
                id=row["id"],
                user_id=row["user_id"],
                chat_provider_id=row["chat_provider_id"],
                title=row["title"],
                provider_name=row["provider_name"],
                created_at=row.get("created_at"),
            )
            for row in response.data
        ]
