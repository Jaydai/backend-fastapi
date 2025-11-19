from pydantic import BaseModel

class NotificationMetadataDTO(BaseModel):
    action_type: str
    action_title_key: str
    action_url: str

class NotificationResponseDTO(BaseModel):
    id: int
    user_id: str
    type: str
    title: str
    body: str
    created_at: str
    read_at: str | None = None
    metadata: NotificationMetadataDTO | None = None

class NotificationStatsResponseDTO(BaseModel):
    total: int
    unread: int

class UpdateNotificationDTO(BaseModel):
    read: bool

class MarkAllReadResponseDTO(BaseModel):
    notifications_updated: int
