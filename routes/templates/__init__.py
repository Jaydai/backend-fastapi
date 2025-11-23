from fastapi import APIRouter

router = APIRouter(prefix="/templates", tags=["Templates"])

from . import (
    search_templates,
    get_all,
    create_template,
    get_template_by_id,
    update_template,
    delete_template,
    track_usage,
    get_versions,
    create_version,
)
