from dataclasses import dataclass


@dataclass
class Block:
    id: str
    type: str
    title: dict[str, str]
    description: dict[str, str] | None
    content: dict[str, str]
    published: bool
    user_id: str
    organization_id: str | None
    workspace_type: str
    created_at: str
    updated_at: str | None
    usage_count: int

@dataclass
class BlockTitle:
    id: str
    title: dict[str, str]
