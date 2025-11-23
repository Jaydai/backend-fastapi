from ast import Dict
from pydantic import BaseModel
from domains.entities import VersionSummary

class CreateTemplateDTO(BaseModel):
    title: str
    description: str | None = None
    content: str
    folder_id: str | None = None  # UUID
    organization_id: str | None = None
    tags: list[str] | None = None
    category: str | None = None
    is_public: bool | None = None
    optimized_for: list[str] | None = None

class UpdateTemplateDTO(BaseModel):
    title: str | None = None
    description: str | None = None
    content: str | None = None
    folder_id: str | None = None  # UUID
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

class TemplateVersionResponseDTO(BaseModel):
    id: int
    template_id: str  # UUID foreign key to template
    name: str
    content: str
    change_notes: str | None = None
    author_id: str
    created_at: str
    updated_at: str | None = None
    status: str
    is_current: bool
    is_published: bool
    usage_count: int
    parent_version_id: int | None = None
    optimized_for: list[str] | None = None

class VersionContentDTO(BaseModel):
    """Version content fetched separately"""
    id: int
    template_id: str
    name: str
    slug: str
    content: str
    change_notes: str | None = None
    author_id: str
    created_at: str
    updated_at: str | None = None
    status: str
    is_current: bool
    is_published: bool
    optimized_for: list[str] | None = None

class TemplateListItemDTO(BaseModel):
    id: str  # UUID in database
    title: str
    description: str | None = None
    folder_id: str | None = None  # UUID
    organization_id: str | None = None
    user_id: str | None = None  # Can be None for public/shared templates
    workspace_type: str
    created_at: str
    updated_at: str | None = None
    tags: list[str] | None = None
    usage_count: int
    current_version_id: int | None = None
    is_free: bool
    is_published: bool

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
    id: str  # UUID in database
    title: str
    description: str | None = None
    folder_id: str | None = None  # UUID
    organization_id: str | None = None
    user_id: str | None = None  # Can be None for public/shared templates
    created_at: str
    updated_at: str | None = None
    usage_count: int
    last_used_at: str | None = None
    current_version_id: int | None = None
    is_published: bool
    versions: list[VersionSummary] = []

class UsageResponseDTO(BaseModel):
    usage_count: int

class TemplateTitleResponseDTO(BaseModel):
    id: str
    title: str
    folder_id: str | None = None  # Needed for tree building

class OrganizationTemplateTitleDTO(BaseModel):
    """Template title for organization context (with localization support)"""
    id: str
    title: str  # Localized title

class TemplateMetadataDTO(BaseModel):
    """Template metadata without content or comments - for efficient loading"""
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
    is_published: bool
    versions: list[VersionSummary] = []  # List of versions without content

class TemplateCountsResponseDTO(BaseModel):
    user_counts: int
    organization_counts: dict[str,int]