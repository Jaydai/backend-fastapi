from pydantic import BaseModel

class CreateTemplateVersionDTO(BaseModel):
    id: int

class TemplateVersionContentDTO(BaseModel):
    """Version content fetched separately"""
    id: int
    content: str