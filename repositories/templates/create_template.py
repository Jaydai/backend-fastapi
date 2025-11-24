from supabase import Client
from domains.entities import Template


def create_template(
    client: Client,
    user_id: str,
    title: dict[str, str],
    description: dict[str, str] | None,
    folder_id: str | None,
    organization_id: str | None,
    tags: list[str] | None,
    workspace_type: str
) -> Template:
    template_data = {
        "user_id": user_id,
        "title": title,
        "description": description,
        "folder_id": folder_id,
        "organization_id": organization_id,
        "tags": tags or [],
        "workspace_type": workspace_type
    }
    response = client.table("prompt_templates").insert(template_data).execute()
    if len(response.data or []) == 0:
        return None
    data = response.data[0]
    return Template(data)
