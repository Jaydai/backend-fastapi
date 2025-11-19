from fastapi import APIRouter

router = APIRouter(prefix="/stats", tags=["User Stats"])

from . import get_stats, get_weekly_chats, get_message_distribution
