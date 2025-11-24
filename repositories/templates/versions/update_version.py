from supabase import Client
from domains.entities import TemplateVersion

def update_version(
    client: Client,
    version_id: int,
    template_id: str,
    content: dict[str, str] | None = None,
    status: str | None = None
) -> TemplateVersion | None:
    """Update a version"""
    update_data = {}
    if content is not None:
        update_data["content"] = content
    if status is not None:
        update_data["status"] = status

    response = client.table("prompt_templates_versions")\
        .update(update_data)\
        .eq("id", version_id)\
        .eq("template_id", template_id)\
        .execute()

    if not response.data:
        return None

    data = response.data[0]
    return TemplateVersion(data)
