from fastapi import APIRouter

router = APIRouter(prefix="/stats", tags=["User Stats"])

from . import get_message_distribution, get_stats, get_weekly_chats  # noqa: E402
