from pydantic import BaseModel


class CreateTemplateVersionDTO(BaseModel):
    id: int


class TemplateVersionContentDTO(BaseModel):
    """Version content fetched separately"""

    id: int
    content: str


class UpdateTemplateVersionDTO(BaseModel):
    content: str | None = None
    description: str | None = None
    status: str | None = None
    is_default: bool | None = None
    published: bool | None = None
    optimized_for: list[str] | None = None


class VersionSlugResponseDTO(BaseModel):
    id: int
    slug: str
