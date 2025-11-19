from dataclasses import dataclass

@dataclass
class NotificationMetadata:
    action_type: str
    action_title_key: str
    action_url: str

@dataclass
class Notification:
    id: int
    user_id: str
    type: str
    title: str
    body: str
    created_at: str
    read_at: str | None = None
    metadata: NotificationMetadata | None = None
