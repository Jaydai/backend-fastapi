"""Template version repository - handles version database operations"""
from supabase import Client
from domains.entities import TemplateVersion
from .get_versions import get_versions

def create_version(
    client: Client,
    template_id: str,
    author_id: str,
    content: dict[str, str],
    name: str | None = None,
    change_notes: dict[str, str] | None = None,
    status: str = "draft",
    optimized_for: list[str] | None = None
) -> TemplateVersion:
    """Create a new template version"""
    # Auto-generate version number if not provided
    if not name:
        existing_versions = get_versions(client, template_id)
        name = f"{len(existing_versions) + 1}.0"

    version_data = {
        "template_id": template_id,
        "author_id": author_id,
        "content": content,
        "name": name,
        "change_notes": change_notes,
        "status": status,
        "optimized_for": optimized_for
    }

    response = client.table("prompt_templates_versions")\
        .insert(version_data)\
        .execute()

    data = response.data[0]
    return TemplateVersion(data)
