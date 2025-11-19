from supabase import Client
from datetime import datetime, timedelta
from domains.entities.message_entities import Message, Chat


class StatsRepository:
    @staticmethod
    def get_user_chats(client: Client, user_id: str, start_date: str | None = None) -> list[Chat]:
        """Get all chats for a user, optionally filtered by start date"""
        query = client.table("chats").select("id, created_at, title, provider_name, chat_provider_id, user_id").eq("user_id", user_id)

        if start_date:
            query = query.gte("created_at", start_date)

        response = query.execute()
        data = response.data or []

        return [
            Chat(
                id=row["id"],
                user_id=row["user_id"],
                chat_provider_id=row["chat_provider_id"],
                title=row["title"],
                provider_name=row["provider_name"],
                created_at=row.get("created_at")
            )
            for row in data
        ]

    @staticmethod
    def get_user_messages(client: Client, user_id: str, start_date: str | None = None) -> list[Message]:
        """Get all messages for a user, optionally filtered by start date"""
        query = client.table("messages").select(
            "id, user_id, chat_provider_id, role, content, created_at, parent_message_provider_id, message_provider_id, model"
        ).eq("user_id", user_id)

        if start_date:
            query = query.gte("created_at", start_date)

        response = query.execute()
        data = response.data or []

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
                parent_message_provider_id=row.get("parent_message_provider_id")
            )
            for row in data
        ]

    @staticmethod
    def get_chat_message_count(client: Client, user_id: str, chat_provider_ids: list[str], start_date: str | None = None) -> list[Message]:
        """Get messages for chats within a date range - only returns chat_provider_id and created_at for counting"""
        query = client.table("messages").select(
            "id, user_id, message_provider_id, content, role, chat_provider_id, model, created_at, parent_message_provider_id"
        ).eq("user_id", user_id)

        # Don't use .in_() if there are too many IDs (causes URI too long error)
        # Instead, rely on start_date filtering and filter by chat IDs in Python
        if start_date:
            query = query.gte("created_at", start_date)

        response = query.execute()
        data = response.data or []

        # Filter by chat_provider_ids in Python if provided
        if chat_provider_ids:
            chat_ids_set = set(chat_provider_ids)
            data = [row for row in data if row.get("chat_provider_id") in chat_ids_set]

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
                parent_message_provider_id=row.get("parent_message_provider_id")
            )
            for row in data
        ]

    @staticmethod
    def get_messages_paginated(client: Client, user_id: str, start_date: str, offset: int = 0, limit: int = 1000) -> list[Message]:
        """Get messages with pagination for large datasets"""
        response = client.table("messages") \
            .select("id, user_id, message_provider_id, chat_provider_id, role, content, created_at, model, parent_message_provider_id") \
            .eq("user_id", user_id) \
            .gte("created_at", start_date) \
            .order("created_at", desc=False) \
            .range(offset, offset + limit - 1) \
            .execute()

        data = response.data or []

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
                parent_message_provider_id=row.get("parent_message_provider_id")
            )
            for row in data
        ]

    @staticmethod
    def get_chats_paginated(client: Client, user_id: str, start_date: str, offset: int = 0, limit: int = 1000) -> list[Chat]:
        """Get chats with pagination for large datasets"""
        response = client.table("chats") \
            .select("id, user_id, chat_provider_id, created_at, provider_name, title") \
            .eq("user_id", user_id) \
            .gte("created_at", start_date) \
            .order("created_at", desc=False) \
            .range(offset, offset + limit - 1) \
            .execute()

        data = response.data or []

        return [
            Chat(
                id=row["id"],
                user_id=row["user_id"],
                chat_provider_id=row["chat_provider_id"],
                title=row["title"],
                provider_name=row["provider_name"],
                created_at=row.get("created_at")
            )
            for row in data
        ]
