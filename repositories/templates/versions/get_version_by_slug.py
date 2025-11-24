"""Repository for getting version by slug."""

from supabase import Client
from domains.entities import TemplateVersion


def get_version_by_slug(
    client: Client,
    template_id: str,
    slug: str
) -> TemplateVersion | None:
    response = client.table("prompt_templates_versions").select(
        "id, template_id, name, slug, content, change_notes, author_id, "
        "created_at, updated_at, status, is_current, is_published, "
        "usage_count, parent_version_id, optimized_for"
    ).eq("template_id", template_id).eq("slug", slug).single().execute()

    if not response.data:
        return None

    return TemplateVersion(**response.data)
