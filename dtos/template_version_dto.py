from pydantic import BaseModel

class VersionSlugResponseDTO(BaseModel):
    id: int
    slug: str