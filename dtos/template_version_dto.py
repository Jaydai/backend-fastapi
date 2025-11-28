from pydantic import BaseModel


class CreateTemplateVersionDTO(BaseModel):
    id: int


class TemplateVersionContentDTO(BaseModel):
    """Version content fetched separately"""
    id: int
    content: str


class UpdateVersionStatusDTO(BaseModel):
    """DTO for updating version status fields"""
    template_id: str
    published: bool | None = None
    status: str | None = None
    is_current: bool | None = None


class VersionSlugResponseDTO(BaseModel):
    id: int
    slug: str