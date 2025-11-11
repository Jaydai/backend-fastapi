from fastapi import APIRouter

router = APIRouter(prefix="/templates", tags=["Templates"])

from . import get_all
