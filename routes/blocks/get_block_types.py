from fastapi import status
from . import router
from services.block_service import BlockService

@router.get("/types", response_model=list[str], status_code=status.HTTP_200_OK)
async def get_block_types() -> list[str]:
    return BlockService.get_block_types()
