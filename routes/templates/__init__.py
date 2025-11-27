from fastapi import APIRouter

router = APIRouter(prefix="/templates", tags=["Templates"])

from . import (  # noqa: E402
    create_template,
    get_template_by_id,
    update_template,
    delete_template,
    track_usage,
    get_versions,
    create_version,
    delete_template,
    get_template_by_id,
    get_version_by_slug,
    get_versions,
    set_default_version,
    track_usage,
    update_template,
)

# Include the versions sub-router for update and delete operations
from .versions import router as versions_router

router.include_router(versions_router)
