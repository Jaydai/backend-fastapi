"""Get template titles repository"""
from supabase import Client
from domains.entities import TemplateTitle


def get_templates_titles(
    client: Client,
    user_id: str | None = None,
    organization_id: str | None = None,
    folder_id: str | None = None,
    limit: int = 100,
    offset: int = 0
) -> list[TemplateTitle]:
    """
    Repository function to fetch template titles from database.
    Applies filters as provided by the service layer.
    """
    query = client.table("prompt_templates").select("id, title, folder_id")

    # Apply filters as provided
    if user_id:
        query = query.eq("user_id", user_id)

    if organization_id:
        query = query.eq("organization_id", organization_id)

    # Don't filter by folder_id - we want ALL templates for tree building
    # The tree building happens client-side using folder_id field

    query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
    response = query.execute()
    templates_data = response.data or []

    templates = [TemplateTitle(**item) for item in templates_data]
    return templates