from fastapi import APIRouter

router = APIRouter(prefix="/folders", tags=["Folders"])

from . import (  # noqa: E402, I001
    get_folders,
    create_folder,
    get_pinned_folders,  # Must be before get_folder to avoid path conflicts
    update_pinned_folders,  # Must be before update_folder to avoid path conflicts
    pin_folder,  # Must be before get_folder to avoid path conflicts
    get_folder,  # /{folder_id} must come after specific paths
    update_folder,
    delete_folder,
)
