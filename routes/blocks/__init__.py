from fastapi import APIRouter

router = APIRouter(prefix="/blocks", tags=["Blocks"])

from . import (
    get_block_types,
    get_blocks,
    create_block,
    get_blocks_by_type,
    get_pinned_blocks,      # Must be before get_block to avoid path conflicts
    update_pinned_blocks,   # Must be before update_block to avoid path conflicts
    seed_sample_blocks,
    get_block,             # /{block_id} must come after specific paths like /pinned
    update_block,
    delete_block,
)
