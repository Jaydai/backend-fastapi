from supabase import Client
from domains.entities import FolderTitle

def get_folders_titles(
    client: Client,
    user_id: str | None = None,
    organization_id: str | None = None,
    parent_folder_id: str | None = None,
    limit: int = 100,
    offset: int = 0
) -> list[FolderTitle]:

    print(f"😎😎😎", parent_folder_id, organization_id, user_id, limit, offset)
    query = client.table("prompt_folders").select("id, title")
    if parent_folder_id is not None:
        query = query.eq("parent_folder_id", parent_folder_id)
    else:
        if organization_id:
            query = query.eq("organization_id", organization_id)
        elif user_id:
            query = query.eq("user_id", user_id)


        query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
        response = query.execute()
        folders_data = response.data or []

        folders = [FolderTitle(**item) for item in folders_data]
        return folders