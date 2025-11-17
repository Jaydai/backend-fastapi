"""
Permission DTOs
Data Transfer Objects for permission-related operations
"""
from pydantic import BaseModel
from domains.enums import RoleEnum, PermissionEnum


class CheckPermissionDTO(BaseModel):
    """DTO for checking if a user has a specific permission"""
    user_id: str
    permission: PermissionEnum
    organization_id: str | None = None  # Check permission in specific org context


class UserRoleResponseDTO(BaseModel):
    """Response DTO for user role information"""
    user_id: str
    role: RoleEnum
    organization_id: str | None = None


class PermissionResponseDTO(BaseModel):
    """Response DTO for permission information"""
    permission: PermissionEnum
    description: str | None = None
    

class RolePermissionsResponseDTO(BaseModel):
    """Response DTO for role with its permissions"""
    role: RoleEnum
    permissions: list[PermissionEnum]
    description: str | None = None
