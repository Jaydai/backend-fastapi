from dataclasses import dataclass

@dataclass
class Folder:
    id: str
    title: dict[str, str]
    description: dict[str, str] | None
    user_id: str | None
    organization_id: str | None
    parent_folder_id: str | None
    workspace_type: str
    created_at: str
    updated_at: str | None

@dataclass
class FolderWithItems:
    folders: list
    templates: list

@dataclass
class FolderTitle:
    id: str
    title: dict[str, str]
