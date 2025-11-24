"""DTO for workspace root content (folders + templates at root level)"""
from pydantic import BaseModel
from dtos.folder_dto import FolderTitleResponseDTO
from dtos.template_dto import TemplateTitleResponseDTO


class WorkspaceRootResponseDTO(BaseModel):
    """Response DTO for workspace root content"""
    folders: list[FolderTitleResponseDTO]
    templates: list[TemplateTitleResponseDTO]
    total_folders: int
    total_templates: int
