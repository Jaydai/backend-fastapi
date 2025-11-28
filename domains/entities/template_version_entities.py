from dataclasses import dataclass


@dataclass
class TemplateVersion:
    id: int
    template_id: str
    name: str
    content: dict[str, str]
    change_notes: dict[str, str] | None
    author_id: str
    created_at: str
    updated_at: str | None
    status: str
    is_current: bool
    published: bool
    usage_count: int
    parent_version_id: int | None
    optimized_for: list[str] | None


@dataclass
class VersionSummary:
    id: int
    name: str
    slug: str
    is_current: bool
    status: str
    optimized_for: list[str] | None = None
    published: bool = False


@dataclass
class VersionContent:
    id: int
    content: dict[str, str]
