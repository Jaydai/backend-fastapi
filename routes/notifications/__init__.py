from fastapi import APIRouter

router = APIRouter(prefix="/notifications", tags=["Notifications"])

from . import (
    get_all,
    get_stats,
    mark_as_read,
    delete_notification
)
