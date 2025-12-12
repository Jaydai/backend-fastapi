from fastapi import APIRouter

router = APIRouter(prefix="/folders", tags=["Folders"])

from . import (  # noqa: E402, I001
    get_folders,
    get_by_scope,  # /by-scope/{scope} must come before /{folder_id}
    create_folder,
    update_pinned_folders,  # Must be before update_folder to avoid path conflicts
    pin_folder,  # Must be before get_folder to avoid path conflicts
    get_folder,  # /{folder_id} must come after specific paths
    update_folder,
    delete_folder,
)
