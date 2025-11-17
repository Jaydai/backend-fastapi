from pydantic import BaseModel


class TemplateTitleResponseDTO(BaseModel):
    id: str
    title: str
