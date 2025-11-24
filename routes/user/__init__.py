from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["User"])

# Sub-routers for nested resources
from .stats import router as stats_router  # noqa: E402
from .usage import router as usage_router  # noqa: E402

router.include_router(stats_router)
router.include_router(usage_router)

# Implemented endpoints
from . import (
    get_profile,
    update_profile,
    update_data_collection,
    me,
    get_ai_coach_insights,
    get_templates_counts,
    get_templates,
    get_folders,
)

# Not implemented yet (501)
from . import (  # noqa: E402
    get_metadata,
    get_profile,
    me,
    update_data_collection,
    update_metadata,
    update_profile,
)
