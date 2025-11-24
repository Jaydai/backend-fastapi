from fastapi import APIRouter

# Create a router without prefix since it will be nested
router = APIRouter()

from . import delete_version, update_version
