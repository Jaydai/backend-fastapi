from dataclasses import dataclass



@dataclass
class Template:
    id: str  # UUID in database
    title: dict[str, str]
    description: dict[str, str] | None
    folder_id: str | None  # UUID
    organization_id: str | None
    user_id: str | None  # Can be None for public/shared templates
    created_at: str
    updated_at: str | None
    usage_count: int
    last_used_at: str | None
    current_version_id: int | None
    is_published: bool

@dataclass
class TemplateVersion:
    id: int
    template_id: str  # UUID foreign key to template
    name: str
    slug: str
    content: dict[str, str]
    change_notes: dict[str, str] | None
    author_id: str
    created_at: str
    updated_at: str | None
    status: str
    is_current: bool
    is_published: bool
    usage_count: int
    parent_version_id: int | None
    optimized_for: list[str] | None

@dataclass
class TemplateWithVersions:
    template: Template
    versions: list[TemplateVersion]
    current_version: TemplateVersion | None

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

@dataclass
class VersionSummary:
    id: int
    name: str
    slug: str
    is_current: bool