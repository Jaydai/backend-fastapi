from pydantic import BaseModel
from enum import Enum

class BlockType(str, Enum):
    ROLE = "role"
    CONTEXT = "context"
    GOAL = "goal"
    TONE_STYLE = "tone_style"
    OUTPUT_FORMAT = "output_format"
    AUDIENCE = "audience"
    EXAMPLE = "example"
    CONSTRAINT = "constraint"
    CUSTOM = "custom"

class CreateBlockDTO(BaseModel):
    type: BlockType
    title: str
    description: str | None = None
    content: str
    published: bool = True
    organization_id: str | None = None
    company_id: str | None = None

class UpdateBlockDTO(BaseModel):
    type: BlockType | None = None
    title: str | None = None
    description: str | None = None
    content: str | None = None
    published: bool | None = None

class BlockResponseDTO(BaseModel):
    id: str
    type: str
    title: str
    description: str | None = None
    content: str
    published: bool
    user_id: str
    company_id: str | None = None
    organization_id: str | None = None
    workspace_type: str
    created_at: str
    updated_at: str | None = None
    usage_count: int

class UpdatePinnedBlocksDTO(BaseModel):
    block_ids: list[str]
