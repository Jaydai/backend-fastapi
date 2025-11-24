"""
Enrichment routes
"""

from fastapi import APIRouter

router = APIRouter()

# Import route handlers to register them
from . import (  # noqa: E402
    enrich_chat,
    enrich_chat_batch,
    enrich_message,
    enrich_message_batch,
    override_quality,
    rated_chats,
    risky_messages,
    whitelist_message,
)

# Import internal routes (no auth required)
from .internal import import_message_rows

__all__ = ["router"]
