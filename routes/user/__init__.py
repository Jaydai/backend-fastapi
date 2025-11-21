from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["User"])

# Sub-routers for nested resources
from .stats import router as stats_router
from .usage import router as usage_router

router.include_router(stats_router)
router.include_router(usage_router)

# Implemented endpoints
from . import (
    get_profile,
    update_profile,
    update_data_collection,
    me,
)

# Not implemented yet (501)
from . import (
    get_metadata,
    update_metadata,
)
