from pydantic import BaseModel
from domains.enums import RoleEnum, PermissionEnum


class CheckPermissionDTO(BaseModel):
    user_id: str
    permission: PermissionEnum
    organization_id: str | None = None  # Check permission in specific org context


class UserRoleResponseDTO(BaseModel):
    user_id: str
    role: RoleEnum
    organization_id: str | None = None


class PermissionResponseDTO(BaseModel):
    permission: PermissionEnum
    description: str | None = None
    

class RolePermissionsResponseDTO(BaseModel):
    role: RoleEnum
    permissions: list[PermissionEnum]
    description: str | None = None
