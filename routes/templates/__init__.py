from fastapi import APIRouter

router = APIRouter(prefix="/templates", tags=["Templates"])

from . import (  # noqa: E402
    create_template,
    create_version,
    delete_template,
    get_template_by_id,
    get_versions,
    set_default_version,
    track_usage,
    update_template,
)

# Include the versions sub-router for update and delete operations
from .versions import router as versions_router  # noqa: E402

router.include_router(versions_router)
