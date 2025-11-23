from supabase import Client
from domains.entities import Template

def update_template(
    client: Client,
    template_id: str,
    title: dict[str, str] | None = None,
    description: dict[str, str] | None = None,
    folder_id: str | None = None,
    tags: list[str] | None = None,
    current_version_id: int | None = None
) -> bool:
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if description is not None:
        update_data["description"] = description
    if folder_id is not None:
        update_data["folder_id"] = folder_id
    if tags is not None:
        update_data["tags"] = tags
    if current_version_id is not None:
        update_data["current_version_id"] = current_version_id

    response = client.table("prompt_templates")\
        .update(update_data)\
        .eq("id", template_id)\
        .execute()

    if len(response.data or []) == 0:
        return None
    data = response.data[0]

    return Template(data)