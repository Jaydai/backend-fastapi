from fastapi import APIRouter

router = APIRouter(prefix="/notifications", tags=["Notifications"])

from . import delete_notification, get_all, get_stats, mark_as_read  # noqa: E402
