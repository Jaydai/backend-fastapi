from fastapi import Depends, Query, HTTPException
from typing import Optional
from . import router
from services import PermissionService, AuthService
from domains.enums import PermissionEnum
from utils import require_permission_in_organization
import logging

logger = logging.getLogger(__name__)


@router.get("", dependencies=[Depends(require_permission_in_organization(PermissionEnum.TEMPLATE_READ))])
async def get_all_templates():
    try:
        logger.info("COUCOU§!!!!!!!!!!!!!!!!")
    except Exception as e:
        logger.error(f"Error fetching templates: {e}")
        raise HTTPException(status_code=500, detail="Internal CUSTOMMMMMMMMMMMMMMM server error") from e
