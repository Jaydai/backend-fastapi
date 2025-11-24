from fastapi import APIRouter

router = APIRouter(prefix="/batch", tags=["Batch"])

from . import save_messages_and_chats  # noqa: E402
