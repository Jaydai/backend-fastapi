from enum import Enum

from pydantic import BaseModel
from domains.enums import BlockTypeEnum


class CreateBlockDTO(BaseModel):
    type: BlockTypeEnum
    title: str
    description: str | None = None
    content: str
    published: bool = True
    organization_id: str | None = None


class UpdateBlockDTO(BaseModel):
    type: BlockTypeEnum | None = None
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
    organization_id: str | None = None
    workspace_type: str
    created_at: str
    updated_at: str | None = None
    usage_count: int


class UpdatePinnedBlocksDTO(BaseModel):
    block_ids: list[str]


class BlockSummaryResponseDTO(BaseModel):
    """Block title response (minimal data for list endpoints)"""
    id: str
    title: str
    type: BlockTypeEnum
    description: str | None = None
    usage_count: int
