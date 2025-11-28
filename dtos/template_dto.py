from pydantic import BaseModel
from domains.entities import VersionSummary

class CreateTemplateDTO(BaseModel):
    title: str
    description: str | None = None
    content: str
    folder_id: str | None = None
    organization_id: str | None = None
    tags: list[str] | None = None
    category: str | None = None
    is_public: bool | None = None
    optimized_for: list[str] | None = None

class UpdateTemplateDTO(BaseModel):
    title: str | None = None
    description: str | None = None
    content: str | None = None
    folder_id: str | None = None
    tags: list[str] | None = None
    category: str | None = None
    is_public: bool | None = None
    is_pinned: bool | None = None
    current_version_id: int | None = None
    version_id: int | None = None
    status: str | None = None

class CreateVersionDTO(BaseModel):
    content: str | None = None
    name: str | None = None
    change_notes: str | None = None
    status: str | None = None
    copy_from_version_id: int | None = None
    optimized_for: list[str] | None = None


class TemplateListItemDTO(BaseModel):
    id: str
    title: str
    description: str | None = None
    folder_id: str | None = None
    organization_id: str | None = None
    user_id: str | None = None
    workspace_type: str
    created_at: str
    updated_at: str | None = None
    tags: list[str] | None = None
    usage_count: int
    current_version_id: int | None = None
    is_free: bool
    published: bool

class TemplateCommentAuthorDTO(BaseModel):
    id: str
    name: str
    avatar: str | None = None

class TemplateCommentDTO(BaseModel):
    id: int
    text: str
    parent_comment_id: str | None = None
    version_id: int | None = None
    created_at: str
    author: TemplateCommentAuthorDTO
    mentions: list = []
    replies: list["TemplateCommentDTO"] = []

class TemplateResponseDTO(BaseModel):
    id: str
    title: str
    description: str | None = None
    folder_id: str | None = None
    organization_id: str | None = None
    user_id: str | None = None
    created_at: str
    updated_at: str | None = None
    usage_count: int
    last_used_at: str | None = None
    current_version_id: int | None = None
    published: bool
    versions: list[VersionSummary] = []

class UsageResponseDTO(BaseModel):
    usage_count: int

class TemplateTitleResponseDTO(BaseModel):
    id: str
    title: str
    folder_id: str | None = None

class OrganizationTemplateTitleDTO(BaseModel):
    """Template title for organization context (with localization support)"""
    id: str
    title: str

class TemplateCountsResponseDTO(BaseModel):
    user_counts: int
    organization_counts: dict[str,int]