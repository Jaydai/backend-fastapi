from fastapi import APIRouter

router = APIRouter(prefix="/invitations", tags=["Invitations"])

# Implemented endpoints
from . import (
    accept,
    decline,
)
