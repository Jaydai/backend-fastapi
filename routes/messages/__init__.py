from fastapi import APIRouter

router = APIRouter(prefix="/messages", tags=["Messages"])

from . import create  # noqa: E402
