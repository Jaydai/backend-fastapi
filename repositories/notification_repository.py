from datetime import UTC, datetime

from supabase import Client

from domains.entities.notification_entities import Notification, NotificationMetadata


class NotificationRepository:
    @staticmethod
    def get_all_notifications(client: Client, user_id: str) -> list[Notification]:
        response = (
            client.table("notifications").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        )

        if not response.data:
            return []

        notifications = []
        for row in response.data:
            metadata = None
            if row.get("metadata"):
                metadata_dict = row["metadata"]
                metadata = NotificationMetadata(
                    action_type=metadata_dict.get("action_type", ""),
                    action_title_key=metadata_dict.get("action_title_key", ""),
                    action_url=metadata_dict.get("action_url", ""),
                )

            read_at = row.get("read_at")
            if read_at == "None":
                read_at = None

            notifications.append(
                Notification(
                    id=row["id"],
                    user_id=row["user_id"],
                    type=row["type"],
                    title=row["title"],
                    body=row["body"],
                    created_at=row["created_at"],
                    read_at=read_at,
                    metadata=metadata,
                )
            )

        return notifications

    @staticmethod
    def get_unread_notifications(client: Client, user_id: str) -> list[Notification]:
        response = (
            client.table("notifications")
            .select("*")
            .eq("user_id", user_id)
            .is_("read_at", "null")
            .order("created_at", desc=True)
            .execute()
        )

        if not response.data:
            return []

        notifications = []
        for row in response.data:
            metadata = None
            if row.get("metadata"):
                metadata_dict = row["metadata"]
                metadata = NotificationMetadata(
                    action_type=metadata_dict.get("action_type", ""),
                    action_title_key=metadata_dict.get("action_title_key", ""),
                    action_url=metadata_dict.get("action_url", ""),
                )

            notifications.append(
                Notification(
                    id=row["id"],
                    user_id=row["user_id"],
                    type=row["type"],
                    title=row["title"],
                    body=row["body"],
                    created_at=row["created_at"],
                    read_at=None,
                    metadata=metadata,
                )
            )

        return notifications

    @staticmethod
    def get_notification_counts(client: Client, user_id: str) -> tuple[int, int]:
        total_response = client.table("notifications").select("id", count="exact").eq("user_id", user_id).execute()

        unread_response = (
            client.table("notifications")
            .select("id", count="exact")
            .eq("user_id", user_id)
            .is_("read_at", "null")
            .execute()
        )

        total_count = total_response.count if hasattr(total_response, "count") else len(total_response.data or [])
        unread_count = unread_response.count if hasattr(unread_response, "count") else len(unread_response.data or [])

        return total_count, unread_count

    @staticmethod
    def mark_notification_as_read(client: Client, notification_id: int, user_id: str) -> bool:
        verification = (
            client.table("notifications").select("id").eq("id", notification_id).eq("user_id", user_id).execute()
        )

        if not verification.data:
            return False

        now = datetime.now(UTC).isoformat()
        response = client.table("notifications").update({"read_at": now}).eq("id", notification_id).execute()

        return bool(response.data)

    @staticmethod
    def mark_all_notifications_as_read(client: Client, user_id: str) -> int:
        unread = client.table("notifications").select("id").eq("user_id", user_id).is_("read_at", "null").execute()

        if not unread.data:
            return 0

        now = datetime.now(UTC).isoformat()
        _ = (
            client.table("notifications")
            .update({"read_at": now})
            .eq("user_id", user_id)
            .is_("read_at", "null")
            .execute()
        )

        return len(unread.data)

    @staticmethod
    def delete_notification(client: Client, notification_id: int, user_id: str) -> bool:
        verification = (
            client.table("notifications").select("id").eq("id", notification_id).eq("user_id", user_id).execute()
        )

        if not verification.data:
            return False

        response = client.table("notifications").delete().eq("id", notification_id).execute()

        return bool(response.data)
