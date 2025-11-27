"""Internal enrichment endpoints - no auth required"""

from fastapi import APIRouter

router = APIRouter()

# Import route handlers
from . import import_message_rows  # noqa: E402

__all__ = ["router"]
