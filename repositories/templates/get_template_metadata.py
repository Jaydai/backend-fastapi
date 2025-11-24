"""Repository for getting template metadata without content."""

from supabase import Client
from domains.entities import Template


def get_template_metadata(client: Client, template_id: str) -> Template | None:
    """
    Get template metadata without content.

    This is optimized for the template detail page initial load,
    fetching only metadata fields (no content, no comments).

    Args:
        client: Supabase client
        template_id: UUID of the template

    Returns:
        Template entity without content, or None if not found
    """
    response = client.table("prompt_templates").select(
        "id, title, description, folder_id, organization_id, user_id, "
        "workspace_type, created_at, updated_at, tags, usage_count, "
        "current_version_id, is_free, is_published"
    ).eq("id", template_id).single().execute()

    if not response.data:
        return None

    # Add empty content field to satisfy Template entity
    data = response.data
    data["content"] = ""

    return Template(**data)
