from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

from . import me

