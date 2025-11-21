from fastapi import Request, HTTPException, status
import logging
from . import router
from services.block_service import BlockService
from dtos import BlockResponseDTO, CreateBlockDTO, BlockType

logger = logging.getLogger(__name__)

@router.post("/seed-samples", response_model=list[BlockResponseDTO], status_code=status.HTTP_201_CREATED)
async def seed_sample_blocks(
    request: Request
) -> list[BlockResponseDTO]:
    try:
        user_id = request.state.user_id
        client = request.state.supabase_client
        locale = request.headers.get("Accept-Language", "en").split(",")[0][:2]

        logger.info(f"User {user_id} seeding sample blocks")

        existing_blocks = BlockService.get_blocks(client, user_id, locale, workspace_type="user")

        if existing_blocks:
            raise HTTPException(status_code=400, detail="User already has blocks")

        sample_blocks = [
            CreateBlockDTO(
                type=BlockType.CONTEXT,
                title="Professional Context",
                description="Sets a professional tone for business communications",
                content="You are a professional assistant helping with business tasks. Maintain a formal and respectful tone.",
                published=True
            ),
            CreateBlockDTO(
                type=BlockType.OUTPUT_FORMAT,
                title="Markdown Output",
                description="Format output as markdown",
                content="Format your response using markdown syntax with proper headings, lists, and code blocks where appropriate.",
                published=True
            ),
            CreateBlockDTO(
                type=BlockType.EXAMPLE,
                title="API Response Example",
                description="Example of a well-structured API response",
                content='{\n  "status": "success",\n  "data": {\n    "id": 123,\n    "name": "Example"\n  }\n}',
                published=True
            ),
            CreateBlockDTO(
                type=BlockType.CONSTRAINT,
                title="Concise Responses",
                description="Keep responses brief and to the point",
                content="Keep your responses concise and focused. Avoid unnecessary elaboration.",
                published=True
            )
        ]

        created_blocks = []
        for sample in sample_blocks:
            block = BlockService.create_block(client, user_id, sample, locale)
            created_blocks.append(block)

        return created_blocks
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error seeding sample blocks: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to seed sample blocks: {str(e)}")
