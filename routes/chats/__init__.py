from fastapi import APIRouter

router = APIRouter(prefix="/chats", tags=["Chats"])

from . import create  # noqa: E402
