from dataclasses import dataclass


@dataclass
class Template:
    id: str
    title: dict[str, str]
    description: dict[str, str] | None
    folder_id: str | None
    organization_id: str | None
    team_id: str | None
    user_id: str | None
    workspace_type: str
    created_at: str
    updated_at: str | None
    usage_count: int
    last_used_at: str | None
    current_version_id: int | None
    published: bool


@dataclass
class TemplateCommentAuthor:
    id: str
    name: str
    avatar: str | None


@dataclass
class TemplateComment:
    id: int
    text: str
    parent_id: int | None
    version_id: int | None
    created_at: str
    author: TemplateCommentAuthor
    mentions: list
    replies: list


@dataclass
class TemplateTitle:
    id: str
    title: dict[str, str]
    folder_id: str | None = None
    team_id: str | None = None
    workspace_type: str | None = None


@dataclass
class TemplateUsage:
    """Template with usage statistics for organization dashboards"""
    id: str
    title: dict[str, str]
    folder_id: str | None = None
    usage_count: int = 0
    last_used_at: str | None = None
    created_at: str | None = None
