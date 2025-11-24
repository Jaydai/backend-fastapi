from dtos.notification_dto import (
    MarkAllReadResponseDTO,
    NotificationMetadataDTO,
    NotificationResponseDTO,
    NotificationStatsResponseDTO,
)
from repositories.notification_repository import NotificationRepository
from supabase import Client


class NotificationService:
    @staticmethod
    def get_all_notifications(client: Client, user_id: str) -> list[NotificationResponseDTO]:
        entities = NotificationRepository.get_all_notifications(client, user_id)

        notifications = []
        for entity in entities:
            metadata_dto = None
            if entity.metadata:
                metadata_dto = NotificationMetadataDTO(
                    action_type=entity.metadata.action_type,
                    action_title_key=entity.metadata.action_title_key,
                    action_url=entity.metadata.action_url,
                )

            notifications.append(
                NotificationResponseDTO(
                    id=entity.id,
                    user_id=entity.user_id,
                    type=entity.type,
                    title=entity.title,
                    body=entity.body,
                    created_at=entity.created_at,
                    read_at=entity.read_at,
                    metadata=metadata_dto,
                )
            )

        return notifications

    @staticmethod
    def get_unread_notifications(client: Client, user_id: str) -> list[NotificationResponseDTO]:
        entities = NotificationRepository.get_unread_notifications(client, user_id)

        notifications = []
        for entity in entities:
            metadata_dto = None
            if entity.metadata:
                metadata_dto = NotificationMetadataDTO(
                    action_type=entity.metadata.action_type,
                    action_title_key=entity.metadata.action_title_key,
                    action_url=entity.metadata.action_url,
                )

            notifications.append(
                NotificationResponseDTO(
                    id=entity.id,
                    user_id=entity.user_id,
                    type=entity.type,
                    title=entity.title,
                    body=entity.body,
                    created_at=entity.created_at,
                    read_at=entity.read_at,
                    metadata=metadata_dto,
                )
            )

        return notifications

    @staticmethod
    def get_notification_stats(client: Client, user_id: str) -> NotificationStatsResponseDTO:
        total, unread = NotificationRepository.get_notification_counts(client, user_id)

        return NotificationStatsResponseDTO(total=total, unread=unread)

    @staticmethod
    def mark_notification_as_read(client: Client, notification_id: int, user_id: str) -> bool:
        return NotificationRepository.mark_notification_as_read(client, notification_id, user_id)

    @staticmethod
    def mark_all_notifications_as_read(client: Client, user_id: str) -> MarkAllReadResponseDTO:
        count = NotificationRepository.mark_all_notifications_as_read(client, user_id)

        return MarkAllReadResponseDTO(notifications_updated=count)

    @staticmethod
    def delete_notification(client: Client, notification_id: int, user_id: str) -> bool:
        return NotificationRepository.delete_notification(client, notification_id, user_id)
