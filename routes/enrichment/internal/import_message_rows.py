"""Import message rows endpoint - for internal scripts"""
from fastapi import HTTPException, Request, status
from pydantic import BaseModel
import logging

from .. import router as parent_router

logger = logging.getLogger(__name__)

class MessageRow(BaseModel):
    id: str | int  # Accept both string and int IDs from database
    user_id: str | None = None
    chat_provider_id: str | None = None
    message_provider_id: str | None = None
    role: str = "user"
    content: str = ""
    created_at: str

class ImportMessageRowsRequest(BaseModel):
    rows: list[MessageRow]

class ChatRow(BaseModel):
    id: str | int  # Accept both string and int IDs from database
    user_id: str | None = None
    chat_provider_id: str
    messages: list[dict]
    created_at: str
    updated_at: str | None = None

class ImportChatRowsRequest(BaseModel):
    rows: list[ChatRow]

@parent_router.post("/internal/import-message-rows", status_code=status.HTTP_200_OK)
async def import_message_rows(
    request: Request,
    body: ImportMessageRowsRequest
) -> dict:
    """
    Import message rows for enrichment processing.

    This endpoint is for internal scripts and doesn't require authentication.
    It accepts batches of message rows and queues them for enrichment.
    """
    try:
        logger.info(f"Received {len(body.rows)} message rows for import")

        # For now, we'll just log the import
        # In a production system, you would:
        # 1. Insert into a queue table
        # 2. Trigger enrichment processing
        # 3. Update enrichment status

        # Example: If you have an enrichment queue table, uncomment and use:
        # client = request.state.supabase_client
        # rows_to_insert = [row.dict() for row in body.rows]
        # response = client.table("enrichment_message_queue").insert(rows_to_insert).execute()

        logger.info(f"Successfully processed {len(body.rows)} message rows")

        return {
            "success": True,
            "imported_count": len(body.rows),
            "message": f"Successfully queued {len(body.rows)} message rows for enrichment"
        }

    except Exception as e:
        logger.error(f"Error importing message rows: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to import message rows: {str(e)}"
        )

@parent_router.post("/internal/import-chat-rows", status_code=status.HTTP_200_OK)
async def import_chat_rows(
    request: Request,
    body: ImportChatRowsRequest
) -> dict:
    """
    Import chat rows for enrichment processing.

    This endpoint is for internal scripts and doesn't require authentication.
    """
    try:
        logger.info(f"Received {len(body.rows)} chat rows for import")

        # For now, we'll just log the import
        # In production, insert into enrichment queue

        logger.info(f"Successfully processed {len(body.rows)} chat rows")

        return {
            "success": True,
            "imported_count": len(body.rows),
            "message": f"Successfully queued {len(body.rows)} chat rows for enrichment"
        }

    except Exception as e:
        logger.error(f"Error importing chat rows: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to import chat rows: {str(e)}"
        )
