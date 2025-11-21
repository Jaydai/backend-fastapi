"""
Enrichment routes
"""
from fastapi import APIRouter

router = APIRouter()

# Import route handlers to register them
from . import enrich_chat
from . import enrich_chat_batch
from . import enrich_message
from . import enrich_message_batch
from . import risky_messages
from . import rated_chats
from . import whitelist_message
from . import override_quality

__all__ = ["router"]
