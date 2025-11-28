from pydantic import BaseModel


class CreateTemplateVersionDTO(BaseModel):
    id: int


class TemplateVersionDTO(BaseModel):
    """Version content fetched separately"""
    id: int
    status: str
    published: bool
    optimized_for: list[str] | None = None
    content: str


class UpdateTemplateVersionDTO(BaseModel):
    name: str | None = None
    content: str | None = None
    description: str | None = None
    status: str | None = None
    is_default: bool | None = None
    published: bool | None = None
    optimized_for: list[str] | None = None

