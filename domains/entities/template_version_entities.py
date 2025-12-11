from dataclasses import dataclass


@dataclass
class TemplateVersion:
    id: int
    template_id: str
    name: str
    content: dict[str, str]
    description: dict[str, str] | None
    author_id: str
    created_at: str
    updated_at: str | None
    status: str
    is_default: bool
    published: bool
    usage_count: int
    parent_version_id: int | None
    optimized_for: list[str] | None

@dataclass
class TemplateVersionUpdate:
    name: str | None
    content: dict[str, str] | None
    description: dict[str, str] | None
    status: str | None
    is_default: bool | None
    published: bool | None
    optimized_for: list[str] | None


@dataclass
class VersionSummary:
    id: int
    name: str
    status: str
    published: bool
    optimized_for: list[str] | None


@dataclass
class VersionDetails:
    id: int
    content: dict[str, str]
    description: dict[str, str] | None
    status: str
    published: bool
    optimized_for: list[str] | None
