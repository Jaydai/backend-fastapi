from pydantic import BaseModel

class CreateFolderDTO(BaseModel):
    title: str
    description: str | None = None
    parent_folder_id: str | None = None
    organization_id: str | None = None

class UpdateFolderDTO(BaseModel):
    title: str | None = None
    description: str | None = None
    parent_folder_id: str | None = None

class FolderResponseDTO(BaseModel):
    id: str
    title: str
    description: str | None = None
    user_id: str | None = None
    organization_id: str | None = None
    parent_folder_id: str | None = None
    workspace_type: str
    created_at: str
    updated_at: str | None = None

class FolderWithItemsDTO(BaseModel):
    folders: list[FolderResponseDTO]
    templates: list
    total_count: int = 0
    has_more: bool = False

class UpdatePinnedFoldersDTO(BaseModel):
    folder_ids: list[str]

class FolderTitleResponseDTO(BaseModel):
    """Folder title response (minimal data for list endpoints)"""
    id: str
    title: str  # Localized title

class OrganizationFolderTitleDTO(BaseModel):
    """Folder title for organization context (with localization support)"""
    id: str
    title: str  # Localized title
