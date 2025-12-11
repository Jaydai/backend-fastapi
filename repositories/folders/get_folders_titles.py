"""Get folder titles repository"""

from supabase import Client

from domains.entities import FolderTitle


def get_folders_titles(
    client: Client,
    user_id: str | None = None,
    organization_id: str | None = None,
    published: bool | None = None,
    parent_folder_id: str | None = None,
    depth: int | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[FolderTitle]:
    """
    Repository function to fetch folder titles from database.
    Applies filters as provided by the service layer.

    Args:
        depth: If provided, limits folder depth relative to parent_folder_id.
               depth=0: Only folders at parent_folder_id level
               depth=1: Folders at parent_folder_id level + their direct children
               depth=None: All folders (current behavior)
    """
    query = client.table("prompt_folders").select("id, title, parent_folder_id")

    if user_id:
        query = query.eq("user_id", user_id)

    if organization_id:
        query = query.eq("organization_id", organization_id)

    if published is not None:
        query = query.eq("published", published)

    query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
    response = query.execute()
    folders_data = response.data or []

    all_folders = [FolderTitle(**item) for item in folders_data]

    if depth is None:
        return all_folders

    return _filter_by_depth(all_folders, parent_folder_id, depth)


def _filter_by_depth(
    folders: list[FolderTitle],
    root_parent_id: str | None,
    max_depth: int
) -> list[FolderTitle]:
    """
    Filter folders by depth relative to root_parent_id.

    depth=0: Only folders where parent_folder_id == root_parent_id
    depth=1: Above + their direct children
    depth=N: Continue N levels deep
    """
    if max_depth < 0:
        return []

    folder_map = {f.id: f for f in folders}
    result_ids: set[str] = set()

    current_level_ids = {
        f.id for f in folders
        if f.parent_folder_id == root_parent_id
    }
    result_ids.update(current_level_ids)

    for _ in range(max_depth):
        next_level_ids: set[str] = set()
        for folder in folders:
            if folder.parent_folder_id in current_level_ids:
                next_level_ids.add(folder.id)
        result_ids.update(next_level_ids)
        current_level_ids = next_level_ids
        if not current_level_ids:
            break

    return [f for f in folders if f.id in result_ids]
