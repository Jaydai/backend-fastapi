"""
Permission DTOs
Data Transfer Objects for permission-related operations
"""
from pydantic import BaseModel
from typing import Optional
from domains.enums import RoleEnum, PermissionEnum


class AssignRoleDTO(BaseModel):
    """DTO for assigning a role to a user"""
    user_id: str
    role: RoleEnum
    organization_id: Optional[str] = None  # None = global role, otherwise org-specific


class RemoveRoleDTO(BaseModel):
    """DTO for removing a role from a user"""
    user_id: str
    organization_id: Optional[str] = None  # None = remove global role, otherwise org-specific


class CheckPermissionDTO(BaseModel):
    """DTO for checking if a user has a specific permission"""
    user_id: str
    permission: PermissionEnum
    organization_id: Optional[str] = None  # Check permission in specific org context


class UserRoleResponseDTO(BaseModel):
    """Response DTO for user role information"""
    user_id: str
    role: RoleEnum
    organization_id: Optional[str] = None


class PermissionResponseDTO(BaseModel):
    """Response DTO for permission information"""
    permission: PermissionEnum
    description: Optional[str] = None
    

class RolePermissionsResponseDTO(BaseModel):
    """Response DTO for role with its permissions"""
    role: RoleEnum
    permissions: list[PermissionEnum]
    description: Optional[str] = None
